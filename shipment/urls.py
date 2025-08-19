from rest_framework.routers import DefaultRouter
from .views import ShipmentViewSet, AddressViewSet, ServiceViewSet

router = DefaultRouter()
router.register('address', AddressViewSet)
router.register('service', ServiceViewSet)
router.register('shipment', ShipmentViewSet)
urlpatterns = router.urls
