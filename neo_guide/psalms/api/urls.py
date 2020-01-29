from django.urls import include
from django.urls import path

from neo_guide.psalms.api.v1.urls import router as v1_router

urlpatterns = [path('v1/', include((v1_router.urls, 'v1-psalms')))]
