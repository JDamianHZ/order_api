from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Supplier, Product, Category
from .serializers import SupplierSerializer, CategorySerializer, ProductSerializer

#CRUD de categorias
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


#CRUD de productos
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

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
    '''
    @action(detail=True, methods=['get'], url_path='low-stock')
    def low_stock(self, request):

        low_stock_product = Product.objects.filter(stock_lt=10)
        suppliers = Supplier.objects.filter(product_in=low_stock_products).distinct()
        serializer = self.get_serializer(suppliers, many=True)
        return Response(serializer.data)
    '''