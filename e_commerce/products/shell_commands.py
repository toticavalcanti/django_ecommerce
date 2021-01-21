'''
# Shell session 1
# python manage.py shell
'''
from tags.models import Tag

qs = Tag.objects.all()
print(qs)

white = Tag.objects.last()
white.title
white.slug
white.active


#É uma forma de procurar somente quem vem do campo many to many
#É um pouco confuso no início, mas na verdade é simples
#Agora a gente tem a possibilidade de pegar todo mundo 
# que tem relação com a tag white nesse caso

# output is a many to many manager
white.products
"""
<django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x7fa2e27707f0>
"""

white.products.all()
"""
This is an actual queryset of PRODUCTS much
like Products.objects.all(), but in this case, it's ALL
of the productstha are related to the "White" tag
"""
white.products.all().first()
"""
return the first instance, if any
"""
exit()
'''
# Shell session 2
# python manage.py shell
'''
from products.models import Product
qs = Product.objects.all()
qs
tshirt = qs.first()
tshirt

tshirt.title
tshirt.description


tshirt.tag  
"""
Raises an error because the Product model doesn`t have a field "tag"
"""
tshirt.tags  
"""
Raises an error because the Product model doesn`t have a field "tags"
"""
tshirt.tag_set
"""
  This works because the Tag model has the "products" field with the ManyToMany to Product
  <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x7fd2e9879f98>
"""

tshirt.tag_set.all()
"""
Returns an actual Queryset of the Tag model, related to this product
"""

tshirt.tag_set.filter(title__iexact='azul')