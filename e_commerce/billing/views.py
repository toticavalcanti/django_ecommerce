from django.shortcuts import render
import stripe
import os

# Supondo que você já carregou as configurações de API do Stripe no settings.py
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY

def payment_method_view(request):
    context = {
        "publish_key": settings.STRIPE_PUB_KEY
    }
    return render(request, 'billing/payment-method.html', context)
