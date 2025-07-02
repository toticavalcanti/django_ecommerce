from decimal import Decimal
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from billing.models import BillingProfile, Card
from orders.models import Order
from products.models import Product
from carts.models import Cart
from django.conf import settings
import stripe
from django.contrib import messages
import json


stripe.api_key = settings.STRIPE_API_KEY

# View para renderizar a página de sucesso do pagamento
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

# View para renderizar a página de falha do pagamento
def payment_failed_view(request):
    return render(request, 'billing/payment-failed.html')

def payment_method_view(request):
    try:
        cart_id = request.session.get("cart_id")
        if not cart_id:
            return redirect("cart:home")

        cart_obj = Cart.objects.filter(id=cart_id).first()
        if not cart_obj:
            return redirect("cart:home")

        order_obj = Order.objects.filter(cart=cart_obj).first()
        if not order_obj:
            return redirect("cart:home")

        # Busca cartões salvos do usuário
        billing_profile, _ = BillingProfile.objects.new_or_get(request)
        saved_cards = []
        if billing_profile:
            saved_cards = Card.objects.filter(
                billing_profile=billing_profile,
                active=True
            ).order_by('-default', '-timestamp')

        context = {
            "publish_key": settings.STRIPE_PUB_KEY,
            "order": order_obj,
            "saved_cards": saved_cards,
            "billing_profile": billing_profile,
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

@csrf_exempt
@require_POST  
def save_payment_method(request):
    """
    Salva o método de pagamento após confirmação bem-sucedida
    """
    try:
        data = json.loads(request.body)
        payment_intent_id = data.get('payment_intent_id')
        
        if not payment_intent_id:
            return JsonResponse({'error': 'PaymentIntent ID required'}, status=400)
        
        # Recupera o PaymentIntent do Stripe
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if payment_intent.status != 'succeeded':
            return JsonResponse({'error': 'Payment not successful'}, status=400)
        
        # Busca o billing profile
        billing_profile, _ = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return JsonResponse({'error': 'Billing profile not found'}, status=400)
        
        # Recupera o PaymentMethod
        payment_method_id = payment_intent.payment_method
        payment_method = stripe.PaymentMethod.retrieve(payment_method_id)
        
        # Salva o cartão
        card, created = Card.objects.add_card_from_stripe_response(
            billing_profile, payment_method
        )
        
        return JsonResponse({
            'success': True,
            'card_saved': created,
            'card_id': card.id,
            'message': 'Cartão salvo com sucesso!' if created else 'Cartão já estava salvo.'
        })
        
    except Exception as e:
        print(f"Erro ao salvar cartão: {str(e)}")
        return JsonResponse({'error': 'Erro interno'}, status=500)

@require_POST
def set_default_card(request, card_id):
    """
    Define um cartão como padrão
    """
    try:
        billing_profile, _ = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            messages.error(request, 'Perfil de cobrança não encontrado.')
            return redirect('billing-payment-method')
        
        card = get_object_or_404(
            Card, 
            id=card_id, 
            billing_profile=billing_profile,
            active=True
        )
        
        card.set_as_default()
        messages.success(request, f'Cartão {card.get_display_name()} definido como padrão.')
        
    except Exception as e:
        messages.error(request, 'Erro ao definir cartão como padrão.')
    
    return redirect('billing-payment-method')

@require_POST
def delete_card(request, card_id):
    """
    Remove um cartão salvo
    """
    try:
        billing_profile, _ = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            messages.error(request, 'Perfil de cobrança não encontrado.')
            return redirect('billing-payment-method')
        
        card = get_object_or_404(
            Card, 
            id=card_id, 
            billing_profile=billing_profile
        )
        
        # Remove do Stripe se possível
        try:
            stripe.PaymentMethod.detach(card.stripe_card_id)
        except stripe.error.StripeError as e:
            print(f"Erro ao remover do Stripe: {e}")
        
        card_name = card.get_display_name()
        card.delete()
        
        messages.success(request, f'Cartão {card_name} removido com sucesso.')
        
    except Exception as e:
        messages.error(request, 'Erro ao remover cartão.')
    
    return redirect('billing-payment-method')

@csrf_exempt
@require_POST
def pay_with_saved_card(request):
    """
    Processa pagamento usando cartão salvo
    """
    try:
        data = json.loads(request.body)
        card_id = data.get('card_id')
        
        if not card_id:
            return JsonResponse({'error': 'Card ID required'}, status=400)
        
        # Busca billing profile e cartão
        billing_profile, _ = BillingProfile.objects.new_or_get(request)
        card = get_object_or_404(Card, stripe_card_id=card_id, billing_profile=billing_profile)
        
        # Busca pedido atual
        cart_id = request.session.get("cart_id")
        cart_obj = Cart.objects.get(id=cart_id)
        order_obj = Order.objects.filter(cart=cart_obj).first()
        total = cart_obj.total + order_obj.shipping_total
        
        # Cria PaymentIntent com cartão salvo
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),
            currency='brl',
            payment_method=card.stripe_card_id,
            confirm=True,
            return_url=request.build_absolute_uri('/billing/payment-success/')
        )
        
        if intent.status == 'succeeded':
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Payment failed'}, status=400)
            
    except Exception as e:
        print(f"Erro ao processar pagamento: {str(e)}")
        return JsonResponse({'error': 'Erro interno'}, status=500)

@csrf_exempt
@require_POST
def create_payment_intent(request):
    data = json.loads(request.body)
    try:
        # Calcular o valor com base nos itens enviados
        # Substitua esta função pela sua lógica de cálculo de preços
        amount = calculate_order_amount(data['items'])

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            payment_method_types=['card'],
        )
        return JsonResponse({'clientSecret': intent.client_secret})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def calculate_order_amount(items):
    cart = Cart.objects.first()  # Ou use um método que pegue o carrinho correto
    total_amount = 0
    for item in items:
        product = Product.objects.get(id=item['id'])
        total_amount += product.price * item['quantity']
    
    # Reutilizar a taxa definida no modelo Cart
    return int(total_amount * Decimal(cart.total / cart.subtotal) * 100)