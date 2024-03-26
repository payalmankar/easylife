from django.urls import path
from .api import *


urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
]
