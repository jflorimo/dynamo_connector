import boto3
from boto3.dynamodb.conditions import Key

from project.settings import env
from .services import (
    get_field_name_list,
    get_dynamodb_attribute_type,
    convert_django_for_dynamo,
)


class Connector:
    def __init__(self, model_class=None):
        self.db = boto3.resource(
            "dynamodb",
            endpoint_url="http://db:8000",
            verify=False,
            aws_access_key_id=env.str("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=env.str("AWS_SECRET_ACCESS_KEY"),
            region_name=env.str("AWS_REGION"),
        )
        self.model = model_class
        if model_class.table_name:
            self.table_name = model_class.table_name
            self.table = self.db.Table(self.table_name)
        else:
            self.table_name = None
            self.table = None

    def create_table(self):
        partition_key = self.model.partition_key
        sort_key = self.model.sort_key
        attribute_list = get_field_name_list(self.model)

        # check partition_key exists in model
        if partition_key not in attribute_list or sort_key not in attribute_list:
            return

        # attribute_definitions = format_attribute_definitions_list(model, attribute_list)
        table = self.db.create_table(
            TableName=self.table_name,
            KeySchema=[
                {"AttributeName": partition_key, "KeyType": "HASH"},  # Partition key
                {"AttributeName": sort_key, "KeyType": "RANGE"},  # Sort key
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": partition_key,
                    "AttributeType": get_dynamodb_attribute_type(
                        self.model, partition_key
                    ),
                },
                {
                    "AttributeName": sort_key,
                    "AttributeType": get_dynamodb_attribute_type(
                        self.model, partition_key
                    ),
                },
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )
        return table

    def select(self, key_tuple_list=None):
        """
        :param key_tuple_list: key and values list [(key, value), ]
        """
        if not key_tuple_list:
            return {}

        key, value = key_tuple_list.pop(0)  # set first key condition expression
        expr = Key(key).eq(value)
        for (
            key,
            value,
        ) in key_tuple_list:  # if remaining key conditions expressions add them
            expr = expr & Key(key).eq(value)

        response = self.table.query(KeyConditionExpression=expr)
        return response["Items"]

    def get(self, key_tuple_list=None):
        res = self.select(key_tuple_list)
        return None if not res else self.select(key_tuple_list)[0]

    def all(self):
        return self.table.scan()["Items"]

    def insert(self, instance):
        """
        :param instance is Django model instance
        """
        data = convert_django_for_dynamo(instance)
        return self.table.put_item(Item={**data})

    def update(self, instance):
        """
        :param instance is Django model instance
        """
        return self.insert(instance)

    def delete(self, key_tuple_list=None):
        """
        :param key_tuple_list: key and values list [(key, value), ]
        """
        if not key_tuple_list:
            return
        return self.table.delete_item(Key=dict(key_tuple_list))
