from django.contrib import admin
from .models import BillingProfile, Card

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = [
        'billing_profile',
        'get_email',
       'brand', 
       'last_four_digits',
       'exp_month', 
       'exp_year',
       'is_expired_display',
       'default',
       'active',
       'timestamp'
    ]
    list_filter = ['brand', 'default', 'active', 'exp_year']
    search_fields = [
        'billing_profile__email', 'brand', 'last_four_digits'
    ]
    readonly_fields = ['stripe_card_id', 'timestamp', 'updated']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('billing_profile')
    
    def get_email(self, obj):
        return obj.billing_profile.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'billing_profile__email'
    
    def is_expired_display(self, obj):
        if obj.is_expired():
            return "⚠️ Expirado"
        return "✅ Válido"
    is_expired_display.short_description = 'Status'
    
    # Ações em massa
    def make_active(self, request, queryset):
        queryset.update(active=True)
    make_active.short_description = "Marcar cartões selecionados como ativos"
    
    def make_inactive(self, request, queryset):
        queryset.update(active=False)
    make_inactive.short_description = "Marcar cartões selecionados como inativos"
    
    actions = [make_active, make_inactive]

admin.site.register(BillingProfile) 