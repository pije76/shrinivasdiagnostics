from django import forms

# from haystack.forms import FacetedSearchForm

PRODUCT_QUANTITY_CHOICES=[(i,str(i)) for i in range(1,21)]

PAYMENT = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CartAddProductForm(forms.Form):
    quantity=forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)
    update=forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 Main St'}))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apartment or suite'}))
    # country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={'class': 'custom-select d-block w-100'}))
    zip = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT)

# class FacetedProductSearchForm(FacetedSearchForm):

#     def __init__(self, *args, **kwargs):
#         data = dict(kwargs.get("data", []))
#         self.categories = data.get('category', [])
#         self.brands = data.get('brand', [])
#         super(FacetedProductSearchForm, self).__init__(*args, **kwargs)

#     def search(self):
#         sqs = super(FacetedProductSearchForm, self).search()
#         if self.categories:
#             query = None
#             for category in self.categories:
#                 if query:
#                     query += u' OR '
#                 else:
#                     query = u''
#                 query += u'"%s"' % sqs.query.clean(category)
#             sqs = sqs.narrow(u'category_exact:%s' % query)
#         if self.brands:
#             query = None
#             for brand in self.brands:
#                 if query:
#                     query += u' OR '
#                 else:
#                     query = u''
#                 query += u'"%s"' % sqs.query.clean(brand)
#             sqs = sqs.narrow(u'brand_exact:%s' % query)
#         return sqs
