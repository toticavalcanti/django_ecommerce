from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from billing.models import BillingProfile
from .forms import AddressForm
from .models import Address

def checkout_address_create_view(request):
    print("========= DEBUG INFO =========")
    print("Method:", request.method)
    print("POST data:", request.POST)
    print("Address Type:", request.POST.get('address_type'))
    form = AddressForm(request.POST or None)
    print("Form is valid:", form.is_valid())
    print("============================")
    
    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            address_type = request.POST.get('address_type', 'shipping')
            print("Address type after validation:", address_type)
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()
            request.session[address_type + "_address_id"] = instance.id
            
            # Se for endereço de cobrança, vai para pagamento
            if address_type == "billing":
                print("Redirecting to payment...")
                return redirect('billing-payment-method')
            return redirect('cart:checkout')

from orders.models import Order # Add this import

def checkout_address_reuse_view(request):
   if request.user.is_authenticated and request.method == "POST":
       billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
       shipping_address = request.POST.get('shipping_address')
       address_type = request.POST.get('address_type')
       
       if shipping_address:
           address = Address.objects.filter(billing_profile=billing_profile, id=shipping_address).first()
           if address:
               order_obj = Order.objects.filter(billing_profile=billing_profile, cart_id=request.session.get('cart_id')).first()
               if order_obj:
                   if address_type == 'shipping':
                       order_obj.shipping_address = address
                   else:
                       order_obj.billing_address = address
                   order_obj.save()
                   
       next_ = request.POST.get('next')
       if url_has_allowed_host_and_scheme(next_, request.get_host()):
           return redirect(next_)
   
   return redirect("cart:checkout")