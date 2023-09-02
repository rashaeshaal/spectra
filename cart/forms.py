from django import forms
from .models import CartItem,Address

# from .models import Order

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'cart', 'quantity',]
        


class BillingDetailsForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone_number', 'address_line_1', 'address_line_2', 'postcode', 'area', 'state']

