from django import forms

from .models import *

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


class Add_BillingForm(forms.Form):
    user = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 Main St'}))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apartment or suite'}))
    # country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={'class': 'custom-select d-block w-100'}))
    state = forms.BooleanField(required=False)
    city = forms.BooleanField(required=False)
    zip = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


class Update_BillingForm(forms.ModelForm):
    # Meta = select2_modelform_meta(Product)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(Div(InlineRadios('')),)

    class Meta:
        model = Address
        fields = (
            'user',
            'address',
            'state',
            'city',
            'zip',
        )
    #     widgets = {
    #         'product_name' : AutoCompleteSelect2Widget(ProductLookup, placeholder='select related item')
    #     }

    # metadata = JSONField()
    # product_name = forms.ModelChoiceField(required=True, label="", queryset=Product.objects.all().order_by('name'), widget=Select2(attrs={'class': "search-container"}))
    # product_name = forms.ModelChoiceField(label="", queryset=Product.objects.distinct('scenarioAreaName'), empty_label="Placeholder")

    # product_name = AutoCompleteSelectField('productlookup', required=False, help_text=None)
    # product_name = AutoCompleteSelectMultipleField('name', required=False, help_text=None)
    # ticker_name = forms.CharField(required=False, label=_('Ticker Name:'), widget=forms.TextInput(attrs={'class': "form-control"}))
    # sector = forms.ModelChoiceField(required=True, label="Sector", queryset=MarketSector.objects.all().order_by('title'), widget=Select2(attrs={'class': "form-control"}))
    # board = forms.ModelChoiceField(required=True, label="Board", queryset=MarketBoard.objects.all().order_by('title'), widget=Select2(attrs={'class': "form-control"}))
    # ipo_date = forms.DateField(required=True, label=_("IPO Date:"), widget=DatePickerInput(format="%d-%m-%Y", attrs={'class': "form-control"}))


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
