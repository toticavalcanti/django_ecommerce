from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path

from products.views import (ProductListView, 
                            product_list_view, 
                            ProductDetailView, 
                            product_detail_view,
                            ProductDetailSlugView,
                            ProductFeaturedListView,
                            ProductFeaturedDetailView)

from .views import home_page, about_page, contact_page, login_page, register_page

urlpatterns = [
	path('', home_page),
	path('about/', about_page),
	path('contact/', contact_page),
        path('login/', login_page),
        path('register/', register_page),
        path('featured/', ProductFeaturedListView.as_view()),
        path('featured/<int:pk>', ProductDetailView.as_view()),
        path('products/', ProductListView.as_view()),
        path('products-fbv/', product_list_view), 
        path('products/<int:pk>', ProductDetailView.as_view()),
        path('products-fbv/<int:pk>', product_detail_view), 
        path('products/<slug:slug>/', ProductDetailSlugView.as_view()),
	path('admin/', admin.site.urls),
        ]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)