from rest_framework import viewsets,permissions
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

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