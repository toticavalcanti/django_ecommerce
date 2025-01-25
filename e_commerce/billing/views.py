from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from billing.models import BillingProfile
from orders.models import Order
from products.models import Product
from carts.models import Cart
from django.conf import settings
import stripe
from django.contrib import messages

stripe.api_key = settings.STRIPE_API_KEY

def payment_success_view(request):
    cart_id = request.session.get("cart_id")
    if cart_id:
        cart_obj = Cart.objects.get(id=cart_id)
        order_obj = Order.objects.filter(cart=cart_obj).first()
        if order_obj:
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
    return render(request, 'billing/payment-success.html')

def payment_failed_view(request):
    return render(request, 'billing/payment-failed.html')

def payment_method_view(request):
    try:
        cart_id = request.session.get("cart_id")
        if not cart_id:
            print(f"Cart ID não encontrado na sessão: {cart_id}")
            return redirect("cart:home")

        cart_obj = Cart.objects.filter(id=cart_id).first()
        if not cart_obj:
            print(f"Cart não encontrado no banco: {cart_id}")
            return redirect("cart:home")

        order_obj = Order.objects.filter(cart=cart_obj).first()
        if not order_obj:
            print("Order não encontrado")
            return redirect("cart:home")

        context = {
            "publish_key": settings.STRIPE_PUB_KEY,
            "order": order_obj,
        }
        return render(request, "billing/payment-method.html", context)

    except Exception as e:
        print(f"Erro: {str(e)}")
        return redirect("cart:home")
@csrf_exempt
@require_POST
def create_checkout_session(request):
    try:
        cart_id = request.session.get("cart_id")
        cart_obj = Cart.objects.get(id=cart_id)
        order_obj = Order.objects.filter(cart=cart_obj).first()
        total = cart_obj.total + order_obj.shipping_total

        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),
            currency='brl',
            automatic_payment_methods={'enabled': True},
        )

        return JsonResponse({
            'clientSecret': intent.client_secret
        })
    except Exception as e:
        print(f"Stripe Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)