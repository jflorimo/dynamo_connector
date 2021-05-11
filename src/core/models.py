from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from dynamodb import Connector


class DynamoCompatibleModel(models.Model):
    class Meta:
        abstract = True

    dynamo = "chips"

    def __init__(self, *args, **kwargs):
        super(DynamoCompatibleModel, self).__init__(*args, **kwargs)
        print("init")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Connector().insert(self.table_name, self)


class Booking(DynamoCompatibleModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_at = models.DateTimeField(default=datetime.now)  # booked at
    date_for = models.DateTimeField(default=datetime.now)  # booked for
    address = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    # dynamo db
    partition_key = "user"
    sort_key = "date_for"
    table_name = "BookingUserByDateFor"

    def __str__(self):
        return f"{self.user} - for {self.date_for} at: {self.address}"


