from django.urls import path
from . import views
from rest_framework import renderers


app_name = "core"

user_list = views.UserViewSet.as_view({"get": "list"})
user_detail = views.UserViewSet.as_view({"get": "retrieve"})

# Booking
booking_list = views.BookingViewSet.as_view({"get": "list", "post": "create"})
booking_detail = views.BookingViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)
booking_highlight = views.BookingViewSet.as_view(
    {"get": "highlight"}, renderer_classes=[renderers.StaticHTMLRenderer]
)


urlpatterns = [
    # path('booking/', booking_detail),
    path("users/", user_list, name="user-list"),
    path("users/<int:pk>/", user_detail, name="user-detail"),
    path("booking/", booking_list, name="booking-list"),
    path("booking/<int:pk>/", booking_detail, name="booking-detail"),
    path("booking/<int:pk>/highlight/", booking_highlight, name="booking-highlight"),
    path("debug/", views.Debug.as_view()),
]
