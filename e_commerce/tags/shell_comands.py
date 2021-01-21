python manage.py shell

from tags.models import Tag
Tag.objects.all()
azul = Tag.objects.last()
azul.title
azul.slug
azul.products
azul.products.all()

from products.models import Product
qs = Product.objects.all()
qs
camisa = qs.first()
camisa.title
camisa.description
camisa.tag
camisa.tags

mas podemos usar tag_set
que é um gerenciador many to many
camisa.tag_set.all()

camisa.tag_set.filter(title__iexact='branca')
camisa.tag_set.filter(title__iexact='branco')