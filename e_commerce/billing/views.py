from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
import json

stripe.api_key = settings.STRIPE_API_KEY

from django.conf import settings
from django.shortcuts import render

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
    # Substitua esta função pela sua lógica de cálculo de preços
    # return sum(item['price'] for item in items)
    return 1500  # preço de exemplo
