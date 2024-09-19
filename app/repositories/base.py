from typing import TypeVar, Generic

import aioboto3
import config
import logging

from pydantic import BaseModel
from abc import ABC, abstractmethod
from botocore.exceptions import ClientError

session = aioboto3.Session()

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)

aws_config = dict(
    endpoint_url=config.DYNAMODB_ENDPOINT_URL,
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    region_name=config.AWS_REGION,
)


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def table_name(self) -> str:
        """
        Pydantic table instance
        """
        pass

    @classmethod
    async def create(cls, schema: T):
        async with session.resource('dynamodb', **aws_config) as dynamodb:
            table = await dynamodb.Table(cls.table_name)
            try:
                await table.put_item(Item=schema.dict())
            except ClientError as e:
                logger.error(f"DynamoDB ClientError: {e}")
                raise
            except Exception as e:
                logger.error(f"DynamoDB Unexpected error: {e}")
                raise
