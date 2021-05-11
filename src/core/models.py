from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from dynamodb import Connector
from dynamodb.services import convert_value_for_dynamo


class DynamoCompatibleModel(models.Model):
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(DynamoCompatibleModel, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Connector(self.__class__).insert(self)


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

    def __from_dynamo__(self, data_dict):
        """
        Convert dynamo dict to Django Booking instance
        :param data_dict: dynamo result dict
        :return: Booking instance
        """
        self.user = User(**{"id": data_dict["user"]})
        self.date_at = datetime.fromtimestamp(data_dict["date_at"])
        self.date_for = datetime.fromtimestamp(data_dict["date_for"])
        self.name = data_dict["name"]
        self.address = data_dict["address"]
        return self

    def __convert_id_to_dynamo_key_list__(self, django_id):
        instance = Booking.objects.get(id=django_id)
        user_key = self.partition_key, instance.user.id
        date_for_key = self.sort_key, convert_value_for_dynamo(instance.date_for)
        return [user_key, date_for_key]

    def __str__(self):
        return f"{self.user} - for {self.date_for} at: {self.address}"
