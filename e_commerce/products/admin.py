from django.contrib import admin
from .models import Product, ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'sku', 'price', 'stock', 'category', 'featured', 'active')  # Colunas exibidas
    list_filter = ('category', 'active', 'featured')  # Filtros laterais
    search_fields = ('title', 'sku', 'description')  # Campos de busca
    prepopulated_fields = {'slug': ('title',)}  # Preenche o slug automaticamente com base no título
    ordering = ('-timestamp',)  # Ordena os produtos do mais recente para o mais antigo

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'alt_text')  # Exibe produto, imagem e texto alternativo
    search_fields = ('product__title', 'alt_text')  # Busca por título do produto ou texto alternativo
    list_filter = ('product',)  # Permite filtrar por produto