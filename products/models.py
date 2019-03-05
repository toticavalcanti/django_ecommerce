from django.db import models
from .utils import unique_slug_generator
from django.db.models.signals import pre_save

#Custom queryset
class ProductQuerySet(models.query.QuerySet):
    
    def active(self):
        return self.filter(active = True)

    def featured(self):
        return self.filter(featured = True, active = True)

class ProductManager(models.Manager):
    
    def get_queryset(self):
        return ProductQuerySet(self.model, using = self._db)
    
    def all(self):
        return self.get_queryset().active()

    def featured(self):
        #self.get_queryset().filter(featured = True)
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id = id)
        if qs.count() == 1:
            return qs.first()
        return None

# Create your models here.
class Product(models.Model): #product_category
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank = True, unique = True)
    description = models.TextField()
    price       = models.DecimalField(decimal_places=2, max_digits=20, default=100.00)
    image       = models.FileField(upload_to = 'products/', null = True, blank = True)
    featured    = models.BooleanField(default = False)
    active      = models.BooleanField(default = True)


    objects = ProductManager()

    def get_absolute_url(self):
        return "/products/{slug}/".format(slug = self.slug)
    
    #python 3
    def __str__(self):
        return self.title
        
    #python 2
    def __unicode__(self):
        return self.title

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender = Product)