from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Booking


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["user", "date_at", "date_for", "address", "name"]


# class DynamoBookingSerializer(serializers.Serializer):
#     user = serializers.IntegerField()
#     date_at = serializers.
