from django.urls import path
from . import views


app_name = "core"

user_list = views.UserViewSet.as_view({"get": "list"})
user_detail = views.UserViewSet.as_view({"get": "retrieve"})

# Django Booking
booking_list = views.BookingViewSet.as_view({"get": "list", "post": "create"})
booking_detail = views.BookingViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)
# Dynamo Booking
dynamo_booking_list = views.DynamoBooking.as_view({"get": "list", "post": "create"})
dynamo_booking_detail = views.DynamoBooking.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    # django,
    path("users/", user_list, name="user-list"),
    path("users/<int:pk>/", user_detail, name="user-detail"),
    path("booking/", booking_list, name="booking-list"),
    path("booking/<int:pk>/", booking_detail, name="booking-detail"),
    # dynamo
    path("dynamo/booking/", dynamo_booking_list, name="dynamo-booking-list"),
    path(
        "dynamo/booking/<int:pk>/", dynamo_booking_detail, name="dynamo-booking-detail"
    ),
    # debug
    path("debug/", views.Debug.as_view()),
]
