from rest_framework.routers import SimpleRouter

from neo_guide.users.api.v1.views import UserViewSet

router = SimpleRouter()
router.register(r'users', UserViewSet)
