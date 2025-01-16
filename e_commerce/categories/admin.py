from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'active', 'timestamp')
    list_filter = ('active', 'parent')  # Filtros para facilitar a navegação
    search_fields = ('name', 'slug', 'description')  # Campos para busca
    prepopulated_fields = {'slug': ('name',)}  # Gera o slug automaticamente