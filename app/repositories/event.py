import logging
import aioboto3
from boto3.dynamodb.conditions import Attr

from schemas.event import EventSchema

from repositories.base import BaseRepository, aws_config
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
session = aioboto3.Session()


class EventRepository(BaseRepository):
    """
    Event Repository class
    """
    table_name = 'events_table'
    model = EventSchema

    @classmethod
    async def find_latest_event_for_city(cls, city: str):
        """
        Method to find the latest event
        """
        async with session.resource('dynamodb', **aws_config) as dynamodb:
            table = await dynamodb.Table(cls.table_name)
            try:
                scan_kwargs = {
                    'FilterExpression': Attr('city').eq(city)
                }
                items = []
                done = False
                start_key = None

                while not done:
                    if start_key:
                        scan_kwargs['ExclusiveStartKey'] = start_key

                    response = await table.scan(**scan_kwargs)
                    items.extend(response.get('Items', []))

                    start_key = response.get('LastEvaluatedKey', None)
                    done = start_key is None

                sorted_items = sorted(
                    items, key=lambda x: x['timestamp'], reverse=True
                )
                latest_item = sorted_items[0] if len(sorted_items) > 0 else None

                return EventSchema(**latest_item) if latest_item else None
            except ClientError as e:
                logger.error(f"DynamoDB ClientError: {e}")
                raise
            except Exception as e:
                logger.error(f"DynamoDB Unexpected error: {e}")
                raise
