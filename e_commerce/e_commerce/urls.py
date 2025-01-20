from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth.views import LogoutView 
from django.urls import path, include
from django.views.generic import TemplateView

from accounts.views import LoginView, RegisterView, LogoutView, guest_register_view
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from billing.views import create_payment_intent, payment_method_view, payment_success_view, payment_failed_view
from .views import (home_page,  
                    about_page, 
                    contact_page
)

urlpatterns = [
    path('', home_page, name='home'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('cart/', include("carts.urls", namespace="cart")),
    path('checkout/address/create/', checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),
    path('login/', LoginView.as_view(), name='login'),  # Login da loja
    path('register/guest/', guest_register_view, name='guest_register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('create-payment-intent', create_payment_intent, name='create-payment-intent'),
    path('billing/payment-method/', payment_method_view, name='billing-payment-method'),
    path('billing/payment-success/', payment_success_view, name='payment-success'),
    path('billing/payment-failed/', payment_failed_view, name='payment-failed'),
    path('bootstrap/', TemplateView.as_view(template_name='bootstrap/example.html')),
    path('search/', include("search.urls", namespace="search")),
    path('products/', include("products.urls", namespace="products")),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)