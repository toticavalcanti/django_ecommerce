from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'address_line_1',
            'address_line_2',
            'city',
            'country',
            'state',
            'postal_code',
        ]

    def clean_address_line_1(self):
        address_line_1 = self.cleaned_data.get('address_line_1')
        if not address_line_1:
            raise forms.ValidationError("Address Line 1 is required.")
        return address_line_1

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if not city:
            raise forms.ValidationError("City is required.")
        return city