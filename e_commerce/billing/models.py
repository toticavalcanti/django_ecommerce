import stripe
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.conf import settings
from accounts.models import GuestEmail

User = settings.AUTH_USER_MODEL
# fulano@mail.com -> pode ter 1.000.000.000 billing profiles
# user fulano@mail.com -> pode ter apenas 1 billing profile
# Initialise environment variables
stripe.api_key = settings.STRIPE_API_KEY

class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user.is_authenticated:
            'logged in user checkout; remember payment stuff'
            obj, created = self.model.objects.get_or_create(
                            user=user, email=user.email)
        elif guest_email_id is not None:
            'guest user checkout; auto reloads payment stuff'
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(
                                            email=guest_email_obj.email)
        else:
            pass
        return obj, created

class BillingProfile(models.Model):
    user = models.OneToOneField(User, null = True, blank = True, on_delete = models.CASCADE)
    email = models.EmailField()
    active =    models.BooleanField(default = True)
    update = models.DateTimeField(auto_now = True)
    timestamp   = models.DateTimeField(auto_now_add = True)
    customer_id = models.CharField(max_length = 120, null = True, blank = True)
    # customer_id no Stripe ou Braintree ou ...
    objects = BillingProfileManager()
    
    def __str__(self):
        return self.email

def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        print("ACTUAL API REQUEST Send to stripe/braintree")
        customer = stripe.Customer.create(
                email = instance.email
            )
        print(customer)
        instance.customer_id = customer.id

pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)

def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user = instance, email = instance.email)

post_save.connect(user_created_receiver, sender = User)

# ==================== CÓDIGO NOVO - MODELO CARD ====================

class CardManager(models.Manager):
    def add_card_from_stripe_response(self, billing_profile, stripe_payment_method):
        """
        Cria ou atualiza um cartão com base na resposta do Stripe PaymentMethod.
        """
        card_data = stripe_payment_method.card
        
        # Verifica se o cartão já existe
        existing_card = self.filter(
            billing_profile=billing_profile,
            stripe_card_id=stripe_payment_method.id
        ).first()
        
        if existing_card:
            return existing_card, False
        
        # Cria novo cartão
        card = self.create(
            billing_profile=billing_profile,
            stripe_card_id=stripe_payment_method.id,
            brand=card_data.brand.title(),
            last_four_digits=card_data.last4,
            exp_month=card_data.exp_month,
            exp_year=card_data.exp_year,
            default=False
        )
        
        # Se é o primeiro cartão, define como padrão
        if not billing_profile.cards.filter(default=True).exists():
            card.default = True
            card.save()
        
        return card, True

class Card(models.Model):
    billing_profile = models.ForeignKey(
        'BillingProfile', 
        on_delete=models.CASCADE,
        related_name='cards'
    )
    stripe_card_id = models.CharField(
        max_length=120, 
        unique=True,
        help_text="ID do PaymentMethod no Stripe"
    )
    brand = models.CharField(
        max_length=120,
        help_text="Marca do cartão (Visa, Mastercard, etc.)"
    )
    last_four_digits = models.CharField(
        max_length=4,
        help_text="Últimos 4 dígitos do cartão"
    )
    exp_month = models.IntegerField(
        help_text="Mês de expiração"
    )
    exp_year = models.IntegerField(
        help_text="Ano de expiração"
    )
    default = models.BooleanField(
        default=False,
        help_text="Cartão padrão para pagamentos"
    )
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    objects = CardManager()
    
    class Meta:
        ordering = ['-default', '-timestamp']
        verbose_name = "Cartão Salvo"
        verbose_name_plural = "Cartões Salvos"
    
    def __str__(self):
        return f"{self.brand} ****{self.last_four_digits}"
    
    def get_display_name(self):
        """Retorna nome amigável para exibição"""
        return f"{self.brand} terminado em {self.last_four_digits}"
    
    def is_expired(self):
        """Verifica se o cartão está expirado"""
        from datetime import datetime
        now = datetime.now()
        return (self.exp_year < now.year or 
                (self.exp_year == now.year and self.exp_month < now.month))
    
    def set_as_default(self):
        """Define este cartão como padrão"""
        # Remove default de outros cartões
        Card.objects.filter(
            billing_profile=self.billing_profile,
            default=True
        ).update(default=False)
        
        # Define este como padrão
        self.default = True
        self.save()

def card_pre_save_receiver(sender, instance, *args, **kwargs):
    """Garante que apenas um cartão seja padrão por billing_profile"""
    if instance.default:
        Card.objects.filter(
            billing_profile=instance.billing_profile,
            default=True
        ).exclude(id=instance.id).update(default=False)

pre_save.connect(card_pre_save_receiver, sender=Card)