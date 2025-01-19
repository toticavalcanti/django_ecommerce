from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail

from addresses.forms import AddressForm
from addresses.models import Address

from billing.models import BillingProfile
from orders.models import Order
from products.models import Product
from .models import Cart, CartProduct

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Cart, CartProduct

def add_to_cart(request):
    if request.method == "POST":
        # Pegando os dados do POST
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity", 1)

        # Validando os dados
        try:
            quantity = int(quantity)
        except ValueError:
            return JsonResponse({"success": False, "message": "Quantidade inválida."})

        # Verificando se o produto existe
        product = get_object_or_404(Product, id=product_id)

        # Obtendo ou criando o carrinho
        cart_obj, _ = Cart.objects.new_or_get(request)

        # Adicionando ou atualizando o produto no carrinho
        cart_product, created = CartProduct.objects.get_or_create(cart=cart_obj, product=product)
        if not created:
            cart_product.quantity += quantity
        else:
            cart_product.quantity = quantity
        cart_product.save()

        # Atualizando o total do carrinho
        cart_obj.update_totals()

        # Calculando o total de itens no carrinho
        total_items = sum(item.quantity for item in cart_obj.cartproduct_set.all())
        request.session['cart_items'] = total_items  # Atualizando a sessão

        return JsonResponse({"success": True, "total_items": total_items})

    # Resposta para requisições que não são POST
    return JsonResponse({"success": False, "message": "Método não permitido."})

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj})
from django.http import JsonResponse

def cart_get_items(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    items = []
    for product in cart_obj.products.all():
        item = {
            'id': product.id,
            'name': product.title,
            'quantity': 1,  # Aqui você deveria usar a quantidade real do produto no carrinho
            'price': str(product.price),
        }
        items.append(item)
    return JsonResponse({'items': items})
def cart_update(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    product_id = request.POST.get("product_id")
    quantity = request.POST.get("quantity", 1)

    try:
        quantity = int(quantity)
    except ValueError:
        quantity = 1

    product_obj = get_object_or_404(Product, id=product_id)

    cart_product, created = CartProduct.objects.get_or_create(cart=cart_obj, product=product_obj)
    if quantity > 0:
        cart_product.quantity = quantity
        cart_product.save()
    else:
        cart_product.delete()

    cart_obj.update_totals()

    request.session['cart_items'] = sum(item.quantity for item in cart_obj.cartproduct_set.all())

    return JsonResponse({
        "success": True,
        "cartItemCount": request.session['cart_items'],
        "subtotal": f"{cart_obj.subtotal:.2f}",  # Subtotal formatado como string
        "total": f"{cart_obj.total:.2f}",        # Total formatado como string
    })

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")  
    
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None

    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        
        # Certifique-se que order_obj existe antes de prosseguir
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()

    # Apenas processe o POST se order_obj existir
    if request.method == "POST" and order_obj is not None:
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return redirect("cart:success")
    
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
    }
    return render(request, "carts/checkout.html", context)

def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})