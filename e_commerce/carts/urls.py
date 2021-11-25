from django.urls import path

app_name = "carts"

from .views import (
                        cart_home, 
                        checkout_home,
                        cart_update,
                        checkout_done_view
                    )

urlpatterns = [
    path('', cart_home, name='home'),
    path('checkout/success/', checkout_done_view, name='success'),
    path('checkout/', checkout_home, name='checkout'),
    path('update/', cart_update, name='update')
]