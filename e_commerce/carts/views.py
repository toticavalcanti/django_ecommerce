from django.http import JsonResponse
from django.shortcuts import render, redirect
from accounts.forms import LoginForm, GuestForm
from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BillingProfile
from orders.models import Order
from products.models import Product
from .models import Cart, CartProduct  # Importação ajustada para incluir CartProduct

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [
        {
            "id": x.product.id,
            "url": x.product.get_absolute_url(),
            "name": x.product.title,
            "price": x.product.price,
            "quantity": x.quantity,  # Adicionada a quantidade
            "total_price": x.product.price * x.quantity,  # Total do item
        }
        for x in cart_obj.cartproduct_set.all()
    ]
    cart_data = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
    return JsonResponse(cart_data)

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj})
from django.http import JsonResponse

def cart_get_items(request):
    """
    Retorna os itens do carrinho em tempo real como uma API JSON.
    """
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    items = []
    for cart_product in cart_obj.cartproduct_set.all():
        item = {
            'id': cart_product.product.id,
            'name': cart_product.product.title,
            'quantity': cart_product.quantity,  # Alterado para refletir a quantidade real
            'price': str(cart_product.product.price),
            'total': str(cart_product.product.price * cart_product.quantity),
        }
        items.append(item)
    response = {
        'items': items,
        'subtotal': str(cart_obj.subtotal),
        'total': str(cart_obj.total),
    }
    return JsonResponse(response)


def cart_update(request):
    product_id = request.POST.get('product_id')
    action = request.POST.get('action')  # 'add' ou 'remove'
    if product_id and action:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Produto não encontrado'}, status=404)
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        cart_product, created = CartProduct.objects.get_or_create(cart=cart_obj, product=product_obj)
        if action == 'add':
            cart_product.quantity += 1
            cart_product.save()
        elif action == 'remove':
            if cart_product.quantity > 1:
                cart_product.quantity -= 1
                cart_product.save()
            else:
                cart_product.delete()
        cart_obj.update_totals()
        return JsonResponse({
            'cartItemCount': cart_obj.cartproduct_set.count(),
            'subtotal': str(cart_obj.subtotal),
            'total': str(cart_obj.total)
        })
    return JsonResponse({'error': 'Dados inválidos'}, status=400)


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.cartproduct_set.count() == 0:
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
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()
    if request.method == "POST":
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
