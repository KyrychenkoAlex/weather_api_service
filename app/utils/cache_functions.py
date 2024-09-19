import aioboto3
import config
import json
import logging

from datetime import datetime, timedelta
from botocore.exceptions import ClientError

from repositories.event import EventRepository

session = aioboto3.Session()
logger = logging.getLogger(__name__)


async def get_s3_weather_cache_for_city(*args, **kwargs):
    aws_config = dict(
        endpoint_url=config.S3_ENDPOINT_URL,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_REGION,
    )

    city = kwargs.get('city')
    if not city:
        raise ValueError("City must be provided as a keyword argument 'city'")

    latest_event = await EventRepository().find_latest_event_for_city(city)

    async with session.client('s3', **aws_config) as s3:
        try:
            now = datetime.utcnow()
            event_time = datetime.fromtimestamp(latest_event.timestamp)
            cache_expiry_time = timedelta(minutes=config.CACHE_EXPIRY_MINUTES)

            time_diff = now - event_time

            if latest_event:
                if time_diff <= cache_expiry_time:
                    obj = await s3.get_object(
                        Bucket=config.S3_BUCKET_NAME,
                        Key=latest_event.s3_filename
                    )

                    data = await obj['Body'].read()
                    return json.loads(data)
            return None
        except ClientError as e:
            logger.error(f"S3 ClientError during cache check: {e}")
            return None
        except Exception as e:
            logger.error(f"S3 Unexpected error during cache check: {e}")
            return None
