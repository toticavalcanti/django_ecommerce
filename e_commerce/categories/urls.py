from django.urls import path
from .views import CategoryListView, CategoryDetailView

app_name = "categories"

urlpatterns = [
    path('', CategoryListView.as_view(), name='list'),
    path('/', CategoryDetailView.as_view(), name='detail'),
]