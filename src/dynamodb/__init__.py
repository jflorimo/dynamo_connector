import boto3
from project.settings import env
from .services import (
    get_field_name_list,
    get_dynamodb_attribute_type,
    format_attribute_definitions_list,
)


class Connector:
    def __init__(self):
        self.db = boto3.resource(
            "dynamodb",
            endpoint_url="http://db:8000",
            verify=False,
            aws_access_key_id=env.str("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=env.str("AWS_SECRET_ACCESS_KEY"),
            region_name=env.str("AWS_REGION"),
        )
        # client = boto3.client(
        #     "dynamodb",
        #     region_name=env.str("AWS_REGION"),
        #     aws_access_key_id=env.str("AWS_ACCESS_KEY_ID"),
        #     aws_secret_access_key=env.str("AWS_SECRET_ACCESS_KEY"),
        # )
        for x in self.db.tables.all():
            print(x)

    # @property
    # def db(self):
    #     return self.db

    def create_table(self, model, *, table_name, partition_key, sort_key):

        attribute_list = get_field_name_list(model)

        # check partition_key exists in model
        if partition_key not in attribute_list or sort_key not in attribute_list:
            return

        # attribute_definitions = format_attribute_definitions_list(model, attribute_list)
        table = self.db.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": partition_key, "KeyType": "HASH"},  # Partition key
                {"AttributeName": sort_key, "KeyType": "RANGE"},  # Sort key
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": partition_key,
                    "AttributeType": get_dynamodb_attribute_type(model, partition_key),
                },
                {
                    "AttributeName": sort_key,
                    "AttributeType": get_dynamodb_attribute_type(model, partition_key),
                },
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )
        return "table"

    def select(self):
        return

    def insert(self):
        return

    def update(self):
        return

    def delete(self):
        return
