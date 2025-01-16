from django.urls import path
from .views import ProductListView, ProductDetailView

app_name = "products"

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('category/<slug:slug>/', ProductListView.as_view(), name='by-category'),
    path('/', ProductDetailView.as_view(), name='detail'),
]