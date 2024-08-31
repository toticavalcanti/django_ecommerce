from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from analytics.models import ObjectViewed
from analytics.mixin import ObjectViewedMixin
from carts.models import Cart
from .models import Product

class ProductFeaturedListView(ListView):
    template_name = "products/list.html"
    
    def get_queryset(self, *args, **kwargs):
        return Product.objects.featured()

class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all().featured()
    template_name = "products/featured-detail.html"

# Class Based View
class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/list.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

# Function Based View
def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)

class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Produto não encontrado!")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()

        # Verifique se o usuário está autenticado e não é um usuário anônimo antes de criar o ObjectViewed
        if self.request.user.is_authenticated and not self.request.user.is_anonymous:
            ObjectViewed.objects.create(
                user=self.request.user,
                content_object=instance  # Usar content_object como indicado no modelo
            )

        # Caso o usuário seja anônimo, não cria o ObjectViewed
        return instance

# Class Based View
class ProductDetailView(ObjectViewedMixin, DetailView):
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Esse produto não existe!")
        return instance

# Function Based View
def product_detail_view(request, pk=None, *args, **kwargs):
    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Esse produto não existe!")

    context = {
        'object': instance
    }
    return render(request, "products/detail.html", context)
