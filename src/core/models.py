from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from dynamodb import Connector
from dynamodb.services import convert_all_values_for_dynamo
import copy as c


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_at = models.DateTimeField(default=datetime.now)  # booked at
    date_for = models.DateTimeField(default=datetime.now)  # booked for
    address = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    # dynamo db
    partition_key = "id"
    sort_key = "user"
    table_name = "BookingByUser"

    def __str__(self):
        return f"{self.user} - for {self.date_for} at: {self.address}"

    def save(self, *args, **kwargs):
        db = Connector()

        if self.pk is not None:
            print(f"UPDATE BOOKING: {self.__dict__}")
            # TODO update here
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
            print(f"CREATE BOOKING: {self.__dict__}")
            insert = db.insert("BookingByUser", self)
