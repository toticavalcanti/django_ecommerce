from django.db import models
from carts.models import Cart

ORDER_STATUS_CHOICES = (
    ('created', 'Criado'),
    ('paid', 'Pago'),
    ('shipped', 'Enviado'),
    ('refunded', 'Devolvido'),
)

class Order(models.Model):
    order_id = models.CharField(max_length = 120, blank = True)
    # billing_profile = ?
    # shipping_address = ?
    # billing_address
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null = True)
    status = models.CharField(max_length = 120, default = 'created', choices = ORDER_STATUS_CHOICES )
    shipping_total = models.DecimalField(default = 5.99, max_digits = 100, decimal_places = 2)
    # Order total = models.DecimalField(default = 0.00, max_digits = 100, decimal_places = 2)

    def __str__(self):
        return self.order_id