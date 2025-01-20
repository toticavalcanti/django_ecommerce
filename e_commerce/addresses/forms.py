from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'street', 
            'number', 
            'complement', 
            'neighborhood', 
            'city',
            'state', 
            'country', 
            'postal_code'
        ]
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'complement': forms.TextInput(attrs={'class': 'form-control'}),
            'neighborhood': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_street(self):
        street = self.cleaned_data.get('street')
        if not street:
            raise forms.ValidationError("Rua é obrigatória.")
        return street

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if not city:
            raise forms.ValidationError("Cidade é obrigatória.")
        return city

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if not postal_code:
            raise forms.ValidationError("CEP é obrigatório.")
        return postal_code