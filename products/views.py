from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Supplier #Product
from .serializers import SupplierSerializer

# Create your views here.

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