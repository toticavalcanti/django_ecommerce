from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product

class SearchProductView(ListView):
    template_name = "products/list.html"
    def get_queryset(self, *args, **kargs):
        request = self.request
        print('Solicitação', request)
        result = request.GET
        print('Resultado: ', result)
        query = result.get('q',  None) # method['q']
        print('Consulta', query)
        if query is not None:
            return Product.objects.filter(title__contains = query)
        return Product.objects.featured()