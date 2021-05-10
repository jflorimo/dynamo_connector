from datetime import datetime
from django.contrib.auth.models import User
from django.db import models


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_at = models.DateTimeField(default=datetime.now)  # booked at
    date_for = models.DateTimeField(default=datetime.now)  # booked for
    address = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user} - for {self.date_for} at: {self.address}"
