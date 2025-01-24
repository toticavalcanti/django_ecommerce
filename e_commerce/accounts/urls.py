from django.urls import path
from .views import LoginView, RegisterView, guest_register_view, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('guest_register/', guest_register_view, name='guest_register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
