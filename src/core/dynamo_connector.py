import boto3
from project.settings import env


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

    def select(self):
        return

    def create(self, partition_key=None, sort_key=None):
        table = self.db.create_table(
            TableName="Movies",
            KeySchema=[
                {"AttributeName": "year", "KeyType": "HASH"},  # Partition key
                {"AttributeName": "title", "KeyType": "RANGE"},  # Sort key
            ],
            AttributeDefinitions=[
                {"AttributeName": "year", "AttributeType": "N"},
                {"AttributeName": "title", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )
        return table

    def update(self):
        return

    def delete(self):
        return
