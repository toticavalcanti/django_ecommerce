from django.http import Http404

from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

from .models import Product

#Class Based View
class ProductListView(ListView):
    #traz todos os produtos do banco de dados sem filtrar nada 
    queryset = Product.objects.all()
    template_name = "products/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context


#Function Based View
def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)

#Class Based View
class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

#Function Based View
def product_detail_view(request, pk = None, *args, **kwargs):
    #instance = Product.objects.get(pk = pk) #get the object id
    #instance = get_object_or_404(Product, pk = pk)
    qs = Product.objects.filter(id = pk)
    if qs.count() == 1:
        instance = qs.first()
    else:
        raise Http404("Esse produto não existe!")

    context = {
        'object': instance
    }
    return render(request, "products/detail.html", context)