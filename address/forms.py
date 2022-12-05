from django import forms

from .models import *
from accounts.models import *

from haystack.forms import FacetedSearchForm, SearchForm
from haystack.inputs import Exact

from crispy_forms.bootstrap import *
from crispy_forms.helper import *
from crispy_forms.layout import *

# from easy_select2 import *

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
    #         'product_title' : AutoCompleteSelect2Widget(ProductLookup, placeholder='select related item')
    #     }

    # metadata = JSONField()
    # product_title = forms.ModelChoiceField(required=True, label="", queryset=Product.objects.all().order_by('name'), widget=Select2(attrs={'class': "search-container"}))
    # product_title = forms.ModelChoiceField(label="", queryset=Product.objects.distinct('scenarioAreaName'), empty_label="Placeholder")

    # product_title = AutoCompleteSelectField('productlookup', required=False, help_text=None)
    # product_title = AutoCompleteSelectMultipleField('name', required=False, help_text=None)
    # ticker_name = forms.CharField(required=False, label=_('Ticker Name:'), widget=forms.TextInput(attrs={'class': "form-control"}))
    # sector = forms.ModelChoiceField(required=True, label="Sector", queryset=MarketSector.objects.all().order_by('title'), widget=Select2(attrs={'class': "form-control"}))
    # board = forms.ModelChoiceField(required=True, label="Board", queryset=MarketBoard.objects.all().order_by('title'), widget=Select2(attrs={'class': "form-control"}))
    # ipo_date = forms.DateField(required=True, label=_("IPO Date:"), widget=DatePickerInput(format="%d-%m-%Y", attrs={'class': "form-control"}))

# ProductFindForm = select2_modelform(Product, attrs={'width': '250px'})
