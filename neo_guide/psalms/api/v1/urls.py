from rest_framework.routers import SimpleRouter

from neo_guide.psalms.api.v1.views import PsalmViewSet

router = SimpleRouter()
router.register(r'psalms', PsalmViewSet)
