from django.db.models import Q
from django.db import models
from e_commerce.utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.urls import reverse
from categories.models import Category  # Importando Category

# Custom queryset
class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(price__icontains=query)
        )
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    
    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)

# Product model
class Product(models.Model):  # product_category
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=100.00)
    discount_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="products")
    sku = models.CharField(max_length=20, unique=True, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})
    
    def get_final_price(self):
        """Retorna o preço com desconto, se disponível."""
        if self.discount_price:
            return self.discount_price
        return self.price

    def has_stock(self):
        """Verifica se o produto tem estoque."""
        return self.stock > 0

    def __str__(self):
        return self.title

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)

# ProductImage model
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, null=True, blank=True)  # Texto alternativo para SEO

    def __str__(self):
        return f"Image for {self.product.title}"
