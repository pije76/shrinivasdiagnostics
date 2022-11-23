from django import forms

from .models import *

# from haystack.forms import FacetedSearchForm

PRODUCT_QUANTITY_CHOICES=[(i,str(i)) for i in range(1,21)]

PAYMENT = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 Main St'}))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apartment or suite'}))
    # country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={'class': 'custom-select d-block w-100'}))
    zip = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT)


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # user = forms.CharField(max_length=100, required=True, label='', widget=forms.TextInput(attrs={'class': "form-control"}))
    # ordered = forms.CharField(max_length=100, required=True, label='', widget=forms.TextInput(attrs={'class': "form-control"}))

    class Meta:
        model = Order
        fields = (
            'item_order',
        )
        # fields = '__all__'
