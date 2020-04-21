from django.urls import include
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from neo_guide.users.api.v1.urls import router as v1_router

urlpatterns = [
    path('v1/', include((v1_router.urls, 'v1-users'))),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
