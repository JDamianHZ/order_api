from rest_framework import serializers
from .models import Category, Product
from .models import Supplier
from inventory.models import InventoryMovement

#Serializador para categorias
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

#Serializador para productos
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True, source='category')

    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'price', 'stock', 'category', 'category_id', 'supplier']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class ProductInventoryMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryMovement
        fields = ["id", "movement_type", "reason", "quantity", "timestamp"]

class ProductInventoryHistorySerializer(serializers.ModelSerializer):
    movements = ProductInventoryMovementSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "sku", "stock", "movements"]