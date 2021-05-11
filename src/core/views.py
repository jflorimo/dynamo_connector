from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from dynamodb import Connector


from .models import Booking
from .serializers import UserSerializer, BookingSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]


class DynamoBooking(viewsets.ModelViewSet):
    queryset = None
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        results = Connector(Booking).all()
        return [Booking().__from_dynamo__(x) for x in results]


class Debug(APIView):
    permission_classes = []

    def get(self, request, format=None):
        dynamo = Connector(Booking)
        # booking_by_user = dynamo.create_table(
        #     Booking, table_name="BookingIdByUser", partition_key="id", sort_key="user"
        # )
        # dynamo.create_table(
        #     Booking, table_name="BookingUserByDateFor", partition_key="user", sort_key="date_for"
        # )
        # dynamo.delete([("user", 1), ("date_for", 1620728015)])
        elem = dynamo.select([("user", 1), ("date_for", 1620746545)])[0]

        response = {
            "table_list": [x.name for x in dynamo.db.tables.all()],
            "values": dynamo.all(),
            "elem": elem,
        }
        return Response(response)
