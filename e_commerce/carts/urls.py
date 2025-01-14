from django.urls import path

from .views import (
    cart_home, 
    checkout_home,
    cart_update,
    checkout_done_view,
    cart_get_items,
    cart_detail_api_view,
)

app_name = "carts"

urlpatterns = [
    path('', cart_home, name='home'),
    path('checkout/success/', checkout_done_view, name='success'),
    path('checkout/', checkout_home, name='checkout'),
    path('update/', cart_update, name='update'),
    path('get-items/', cart_get_items, name='cart-get-items'),
    path('api/', cart_detail_api_view, name='api'),
]
