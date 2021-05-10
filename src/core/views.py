from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .dynamo_connector import Connector


from .models import Booking
from .serializers import UserSerializer, BookingSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Booking.objects.all().order_by("-date_for")
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]


class Debug(APIView):
    permission_classes = []

    def get(self, request, format=None):
        print("YOLO")
        dynamo = Connector()
        table = dynamo.create()

        return Response({"test": table.table_status})
