from django.urls import path, include
from .v0 import urls as v0_urls

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="API Document",
      default_version='v0'
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("document/", schema_view.with_ui('swagger', cache_timeout=0), name="api-document"),
    path("v0/", include(v0_urls), name="v0"),
]


