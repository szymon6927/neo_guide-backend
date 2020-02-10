from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from neo_guide.core.views import HealthCheckView

schema_view = get_schema_view(
    openapi.Info(title='neo_guide API', default_version='v1'),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
)

# api routers
api_urlpatterns = [path('api/', include('neo_guide.psalms.api.urls'))]


# Django Admin
admin.site.site_header = "Neo Guide"
admin.site.site_title = "Neo Guide"
admin.site.index_title = "Welcome to Neo Guide admin panel"

urlpatterns = [
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('health', HealthCheckView.as_view(), name='health-check'),
    path('', RedirectView.as_view(url=reverse_lazy('admin:index')), name='homepage'),
    path(settings.ADMIN_URL, admin.site.urls),
    # api urls
    *api_urlpatterns,
]

if settings.DEBUG:
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
