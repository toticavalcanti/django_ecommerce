from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
User = settings.AUTH_USER_MODEL
# fulano@mail.com -> pode ter 1.000.000.000 billing profiles
# user fulano@mail.com -> pode ter apenas 1 billing profile
class BillingProfile(models.Model):
    user = models.OneToOneField(User, null = True, blank = True, on_delete = models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default = True)
    update = models.DateTimeField(auto_now = True)
    timestamp = models.DateTimeField(auto_now_add = True)
    # customer_id no Stripe ou Braintree ou ...

    def __str__(self):
        return self.email

def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user = instance, email = instance.email)

post_save.connect(user_created_receiver, sender = User)