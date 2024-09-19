import json
import logging
import aioboto3

from fastapi import HTTPException
from botocore.exceptions import ClientError
import config

logger = logging.getLogger(__name__)

session = aioboto3.Session()


class S3Service:
    def __init__(self) -> None:
        self.aws_config = dict(
            endpoint_url=config.S3_ENDPOINT_URL,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            region_name=config.AWS_REGION,
        )

    async def upload_json(self, filename: str, data: dict) -> str:
        """
        Method for uploading json data to s3 bucket
        :param filename:
        :param data:
        :return:
        """

        async with session.client('s3', **self.aws_config) as s3:
            try:
                body = json.dumps(data)
                logger.info(f"S3 ClientError: {body} {filename}")
                await s3.put_object(
                    Bucket=config.S3_BUCKET_NAME,
                    Key=filename,
                    Body=body
                )

                return (
                    f"{config.S3_ENDPOINT_URL}/"
                    f"{config.S3_BUCKET_NAME}/{filename}")
            except ClientError as e:
                logger.error(f"S3 ClientError: {e}")

                raise HTTPException(
                    status_code=500,
                    detail="Error uploading to storage."
                )
            except Exception as e:
                logger.error(f"S3 Unexpected error: {e}")
                raise HTTPException(
                    status_code=500,
                    detail="Internal server error."
                )
