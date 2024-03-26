from django.urls import path, include

from .authentication import urls as authentication_urls

urlpatterns = [
    path("auth/", include(authentication_urls), name="authentication_urls"),
]