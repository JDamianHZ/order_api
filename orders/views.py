from django.db.models import Prefetch, QuerySet
from rest_framework import viewsets, permissions
from django.utils.dateparse import parse_date
from .models import Order, OrderItem
from .serializers import OrderSerializer
from rest_framework.request import Request

# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self) -> QuerySet[Order]:
        request: Request = self.request
        qs = (
            Order.objects.all()
            .select_related()
            .prefetch_related(Prefetch("items", queryset=OrderItem.objects.select_related("product")))
            .order_by("-created_at")
        )
        
        status_val = request.query_params.get("status")
        if status_val:
            qs = qs.filter(status=status_val)
            
        date_from = parse_date(request.query_params.get("date_from") or None)
        date_to = parse_date(request.query_params.get("date_to") or None)
        if date_from:
            qs = qs.filter(created_at__gte=date_from)
        else:
            qs = qs.filter(created_at__lte=date_to)
        return qs
    