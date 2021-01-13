from django.shortcuts import render

from products.models import Product
from .models import Cart

def cart_home(request):
    cart_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {})

def cart_update(request):
    product_id = 5
    # Pega o produto com id 5
    product_obj = Product.objects.get(id=product_id)
    # Cria ou pega a instância já existente do carrinho
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    # E o produto se adiciona a instância do campo M2M 
    cart_obj.products.add(product_obj) # cart_obj.products.add(product_id)
    #cart_obj.products.remove(product_obj) # cart_obj.products.remove(product_id)
    return redirect(product_obj.get_absolute_url())