from django.db import models
#from products.models import Product

# Create your models here.

class InventoryMovement(models.Model):
    MOVEMENT_TYPES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]

    REASONS = [
        ('compra', 'Compra'),
        ('venta', 'Venta'),
        ('ajuste', 'Ajuste'),
    ]
    '''
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name= 'movements')
    quantity = models.PositiveIntegerField()
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPES)
    reason = models.CharField(max_length=10, choices=REASONS)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.movement_type} ({self.quantity})"
    '''