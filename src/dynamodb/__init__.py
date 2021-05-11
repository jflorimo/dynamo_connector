import boto3
from boto3.dynamodb.conditions import Key
from django.forms.models import model_to_dict

from project.settings import env
from .services import (
    get_field_name_list,
    get_dynamodb_attribute_type,
    convert_all_values_for_dynamo,
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
        return table

    def select(self, table_name, key_tuple_list=None):
        """
        :param key_tuple_list: key and values list [(key, value), ]  used for sort
        """
        table = self.db.Table(table_name)
        if not key_tuple_list:
            return {}

        key, value = key_tuple_list.pop(0)  # set first key condition expression
        expr = Key(key).eq(value)
        for (
            key,
            value,
        ) in key_tuple_list:  # if remaining key conditions expressions add them
            expr = expr & Key(key).eq(value)

        response = table.query(KeyConditionExpression=expr)
        return response["Items"]

    def select_all(self, table_name):
        return self.db.Table(table_name).scan()

    def insert(self, table_name, instance):
        table = self.db.Table(table_name)
        data = model_to_dict(instance)
        data = convert_all_values_for_dynamo(data)
        return table.put_item(Item={**data})

    def update(self, table_name, instance):
        return self.insert(table_name, instance)

    def delete(self, table_name, key_tuple_list=None):
        table = self.db.Table(table_name)
        if not key_tuple_list:
            return
        return table.delete_item(Key=dict(key_tuple_list))
