from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    LoginAPIView,
    RegistrationAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    AccessCheckAPIView,
)

app_name = "authentication"
urlpatterns = [
    path("info/", UserRetrieveAPIView.as_view()),
    path("update/", UserUpdateAPIView.as_view()),
    path("signup/", RegistrationAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("check/", AccessCheckAPIView.as_view()),
]
