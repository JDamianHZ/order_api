from django.db import transaction
from django.db.models import Prefetch, QuerySet
from rest_framework import viewsets, permissions, status
from django.utils.dateparse import parse_date
from inventory.models import InventoryMovement
from products.models import Product
from .models import Order, OrderItem
from .serializers import OrderSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import F

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

        date_from_raw = request.query_params.get('date_from')
        if date_from_raw:
            df = parse_date(date_from_raw)
            if df:
                qs = qs.filter(created_at__date__gte=df)

        date_to_raw = request.query_params.get('date_to')
        if date_to_raw:
            dt = parse_date(date_to_raw)
            if dt:
                qs = qs.filter(created_at__date__lte=dt)

        return qs

    @action(detail=True, methods=["patch"], url_path="complete")
    def complete(self, request, pk=None):
        order = self.get_object()

        if order.status == "completed":
            return Response({"detail": "Order is already completed."}, status=status.HTTP_400_BAD_REQUEST)
        if order.status == "canceled":
            return Response({"detail": "Canceled orders cannot be completed."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():

            already_applied = True
            for item in order.items.select_related("product").all():
                exists_mv = InventoryMovement.objects.filter(
                    product=item.product,
                    movement_type="salida",
                    reason="venta",
                    timestamp__gte=order.created_at
                ).exists()
                if not exists_mv:
                    already_applied = False
                    break

            if not already_applied:

                insuficientes = []
                for item in order.items.select_related("product").all():
                    if item.product.stock < item.quantity:
                        insuficientes.append({
                            "product_id": item.product_id,
                            "name": item.product.name,
                            "requested": item.quantity,
                            "available": item.product.stock,
                        })
                if insuficientes:
                    return Response(
                        {"detail": "Insufficient stock for some products.", "items": insuficientes},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                for item in order.items.select_related("product").all():
                    Product.objects.filter(pk=item.product_id).update(stock=F("stock") - item.quantity)
                    InventoryMovement.objects.create(
                        product=item.product,
                        quantity=item.quantity,
                        movement_type="salida",
                        reason="venta",
                    )

            order.status = "completed"
            order.save(update_fields=["status"])

        return Response(self.get_serializer(order).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], url_path="cancel")
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status == "completed":
            return Response({"detail": "Completed orders cannot be canceled."}, status=400)
        if order.status == "canceled":
            return Response({"detail": "Order is already canceled."}, status=400)
        order.status = "canceled"
        order.save(update_fields=["status"])
        return Response(self.get_serializer(order).data)