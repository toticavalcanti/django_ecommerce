from django.urls import path

from .views import (
    cart_home, 
    checkout_home,
    cart_update,
    checkout_done_view,
    cart_get_items,
    add_to_cart,
)

app_name = "carts"

urlpatterns = [
    path('', cart_home, name='home'),
    path('checkout/success/', checkout_done_view, name='success'),
    path('checkout/', checkout_home, name='checkout'),
    path('update/', cart_update, name='update'),
    path('get-items/', cart_get_items, name='cart-get-items'),
    path('add/', add_to_cart, name='add_to_cart'),
]
