# realtime_poll/urls.py
from django.contrib import admin
from django.urls import path, include
from accounts.views import home  # if you have home view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Polling API",
      default_version='v1',
      description="API for real-time polling",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/polls/', include('polls.urls')),
    path('', home),  # optional home page
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
