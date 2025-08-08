from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Supplier, Product, Category
from .serializers import SupplierSerializer, CategorySerializer, ProductSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .permissions import IsAdminUserCustom

#CRUD de categorias
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


#CRUD de productos
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUserCustom()]
        return [IsAuthenticatedOrReadOnly()]

    @extend_schema(
        summary="List all products",
        responses={200: OpenApiResponse(response=ProductSerializer(many=True))}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a product",
        responses={200: OpenApiResponse(response=ProductSerializer)}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new product (admin only)",
        responses={
            201: ProductSerializer,
            403: OpenApiResponse(description="Not authorized (requires admin)")
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update a product (admin only)",
        responses={
            200: ProductSerializer,
            403: OpenApiResponse(description="Not authorized (requires admin)")
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a product (admin only)",
        responses={204: OpenApiResponse(description="Product deleted")}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    #Filtro por categoria
    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    @action(detail=True, methods=['get'], url_path='low-stock')
    @extend_schema(summary="Suppliers with products below 10 Units")
    def low_stock(self, request):

        low_stock_products = Product.objects.filter(stock_lt=10)
        suppliers = Supplier.objects.filter(product_in=low_stock_products).distinct()
        serializer = self.get_serializer(suppliers, many=True)
        return Response(serializer.data)