from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from products.models import Product
from django.conf import settings
import stripe
import json

stripe.api_key = settings.STRIPE_API_KEY

# View para renderizar a página de sucesso do pagamento
def payment_success_view(request):
    return render(request, 'billing/payment-success.html')

# View para renderizar a página de falha do pagamento
def payment_failed_view(request):
    return render(request, 'billing/payment-failed.html')

def payment_method_view(request):
    # Adicione um log para verificar se a chave está sendo passada
    # print(f"Publish Key na view: {settings.STRIPE_PUB_KEY}")
    context = {'publish_key': settings.STRIPE_PUB_KEY}
    return render(request, 'billing/payment-method.html', context)

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
    total_amount = 0
    for item in items:
        product = get_object_or_404(Product, id=item['id'])
        total_amount += product.price * item['quantity']
    return int(total_amount * 100)  # o valor deve estar em centavos