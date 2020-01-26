from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from neo_guide.core.views import health

schema_view = get_schema_view(
    openapi.Info(title='neo_guide API', default_version='v1'),
    public=True,
    permission_classes=(permissions.IsAdminUser, )
)

urlpatterns = [
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('health', health),
    path(settings.ADMIN_URL, admin.site.urls),
    # Your stuff: custom urls includes go here
]

if settings.DEBUG:
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
