from django.db import models

#Modelo de categoria
class Category (models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

#Modelo de Productos
class Product (models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50,unique =True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)

    def __str__(self):
        return self.name