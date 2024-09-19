import boto3
from botocore.exceptions import ClientError

import config

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=config.DYNAMODB_ENDPOINT_URL,
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    region_name=config.AWS_REGION
)


def create_table(table_name: str, key_schema: list, attribute_definitions: list):
    """
    Creates table in DynamoDB

    :param table_name:
    :param key_schema:
    :param attribute_definitions:
    :return:
    """
    existing_tables = dynamodb.meta.client.list_tables()['TableNames']
    if table_name not in existing_tables:
        try:
            table = dynamodb.create_table(
                TableName=table_name,
                KeySchema=key_schema,
                AttributeDefinitions=attribute_definitions,
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            table.meta.client.get_waiter('table_exists').wait(
                TableName=table_name)
            print(f"Table '{table_name}' created successfully on startup.")
        except ClientError as e:
            print(f"Error creating table: {e}")
