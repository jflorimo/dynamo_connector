from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from dynamodb import Connector
from dynamodb.viewset import DynamoViewset


from .models import Booking
from .serializers import UserSerializer, BookingSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Booking to be viewed or edited.
    """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = []


class DynamoBooking(DynamoViewset):
    queryset = None
    model_class = Booking  # needed to use DynamoViewset
    serializer_class = BookingSerializer
    permission_classes = []


class Debug(APIView):
    permission_classes = []

    def get(self, request, format=None):
        dynamo = Connector(Booking)
        elem = dynamo.get([("user", 1), ("date_for", 1620746545)])
        response = {
            "table_list": [x.name for x in dynamo.db.tables.all()],
            "values": dynamo.all(),
            "elem": elem,
        }
        return Response(response)
