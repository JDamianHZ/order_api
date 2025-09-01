from rest_framework.routers import DefaultRouter
from .views import ShipmentViewSet, AddressViewSet, ServiceViewSet

router = DefaultRouter()
router.register('address', AddressViewSet, basename='address')
router.register('service', ServiceViewSet, basename='service')
router.register('shipment', ShipmentViewSet, basename='shipment')
urlpatterns = router.urls