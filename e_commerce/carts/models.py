from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from products.models import Product

User = settings.AUTH_USER_MODEL


class CartProduct(models.Model):
    """
    Modelo intermediário para gerenciar produtos no carrinho com quantidades.
    """
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            return qs.first(), new_obj
        else:
            cart_obj = self.new()
            request.session["cart_id"] = cart_obj.id
            new_obj = True
            return cart_obj, new_obj

    def new(self):
        return self.model.objects.create()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product, through='CartProduct', blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    def update_totals(self):
        """
        Atualiza os totais do carrinho com base na quantidade dos produtos.
        """
        subtotal = sum(
            cart_product.product.get_final_price() * cart_product.quantity
            for cart_product in self.cartproduct_set.all()
        )
        self.subtotal = subtotal
        self.total = subtotal  # Substitua se tiver taxa de entrega
        self.save()


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = Decimal(instance.subtotal)  # Adicione taxa se necessário
    else:
        instance.total = 0.00


pre_save.connect(pre_save_cart_receiver, sender=Cart)
