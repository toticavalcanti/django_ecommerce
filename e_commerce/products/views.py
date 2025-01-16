from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from analytics.models import ObjectViewed
from analytics.mixin import ObjectViewedMixin
from carts.models import Cart
from .models import Product


class ProductFeaturedListView(ListView):
    """Listagem de produtos destacados."""
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        return Product.objects.featured()


class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
    """Detalhes de um produto destacado."""
    queryset = Product.objects.featured()
    template_name = "products/featured-detail.html"


class ProductListView(ListView):
    """Listagem de produtos disponíveis."""
    queryset = Product.objects.all()
    template_name = "products/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context


def product_list_view(request):
    """Listagem de produtos usando Function-Based View."""
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    """Detalhes de um produto utilizando slug como identificador."""
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
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

        # Cria o evento ObjectViewed se o usuário estiver autenticado
        if self.request.user.is_authenticated:
            ObjectViewed.objects.create(
                user=self.request.user,
                content_object=instance
            )
        return instance


class ProductDetailView(ObjectViewedMixin, DetailView):
    """Detalhes de um produto utilizando o ID como identificador."""
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Esse produto não existe!")
        return instance


def product_detail_view(request, pk=None, *args, **kwargs):
    """Detalhes de um produto utilizando Function-Based View."""
    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Esse produto não existe!")

    context = {
        'object': instance
    }
    return render(request, "products/detail.html", context)