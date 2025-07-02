from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth.views import LogoutView 
from django.urls import path, include
from django.views.generic import TemplateView

from carts.views import cart_detail_api_view
from accounts.views import LoginView, RegisterView, LogoutView, guest_register_view
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from billing.views import (
    create_payment_intent, 
    payment_method_view, 
    payment_success_view, 
    payment_failed_view, 
    save_payment_method, 
    set_default_card, 
    delete_card,
    pay_with_saved_card
)
from .views import (
    home_page,  
    about_page, 
    contact_page
)

urlpatterns = [
    # === CORE PAGES ===
    path('', home_page, name='home'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    
    # === APPS ===
    path('cart/', include("carts.urls", namespace="cart")),
    path('search/', include("search.urls", namespace="search")),
    path('products/', include("products.urls", namespace="products")),
    
    # === API ENDPOINTS ===
    path('api/cart/', cart_detail_api_view, name='api-cart'),
    
    # === AUTH ===
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/guest/', guest_register_view, name='guest_register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # === CHECKOUT & ADDRESSES ===
    path('checkout/address/create/', checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),
    
    # === BILLING & PAYMENTS ===
    path('billing/payment-method/', payment_method_view, name='billing-payment-method'),
    path('billing/payment-success/', payment_success_view, name='payment-success'),
    path('billing/payment-failed/', payment_failed_view, name='payment-failed'),
    path('billing/create-payment-intent/', create_payment_intent, name='create-payment-intent'),
    path('billing/save-payment-method/', save_payment_method, name='save-payment-method'),
    path('billing/set-default-card/<int:card_id>/', set_default_card, name='set-default-card'),
    path('billing/delete-card/<int:card_id>/', delete_card, name='delete-card'),
    path('billing/pay-with-saved-card/', pay_with_saved_card, name='pay-with-saved-card'),
    # === ADMIN & MISC ===
    path('bootstrap/', TemplateView.as_view(template_name='bootstrap/example.html')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)