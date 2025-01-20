from django.db import models
from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)

class Address(models.Model):
    billing_profile = models.ForeignKey(
        BillingProfile, 
        on_delete=models.CASCADE,
        null=True,  # Permite nulo temporariamente
        blank=True  # Permite formulários vazios temporariamente
    )
    address_type = models.CharField(
        max_length=120, 
        choices=ADDRESS_TYPES, 
        default="shipping"
    )
    street = models.CharField(max_length=255, null=False, blank=False, default="")
    complement = models.CharField(max_length=255, null=True, blank=True, default="")
    neighborhood = models.CharField(max_length=255, null=True, blank=True, default="")
    number = models.CharField(max_length=10, null=True, blank=True, default="")
    city = models.CharField(max_length=100, null=False, blank=False, default="")
    state = models.CharField(max_length=100, null=False, blank=False, default="")
    country = models.CharField(max_length=100, null=False, blank=False, default="")
    postal_code = models.CharField(max_length=20, null=False, blank=False, default="")

    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}, {self.state} ({self.postal_code})"

    def get_address(self):
        address_parts = [
            f"{self.street}, {self.number}",
            self.complement if self.complement else "",
            self.neighborhood if self.neighborhood else "",
            f"{self.city}, {self.state}",
            self.postal_code,
            self.country
        ]
        return "\n".join(filter(None, address_parts))