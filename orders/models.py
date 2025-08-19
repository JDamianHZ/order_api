from django.db import models
from products.models import Product

# Create your models here.

class Order(models.Model):
    PENDING = "pendiente"
    COMPLETED = "completada"
    CANCELED = "cancelada"
    STATUS_CHOICES = (
        (PENDING, "Pendiente"),
        (COMPLETED, "Completada"),
        (CANCELED, "Cancelada"),
    )

    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order # {self.id} - {self.customer_name}"

class OrderItem(models.Model):

    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="items", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total(self):
        return self.quantity * self.price