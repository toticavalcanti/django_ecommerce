from django.urls import path
from .views import custom_logout_view

app_name = 'accounts'

urlpatterns = [
    # Outras rotas do app
    path('logout/', custom_logout_view, name='logout'),
]