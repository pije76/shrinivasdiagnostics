from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# from django.contrib.postgres.fields.jsonb import JSONField

from shop.models import *
from .models import *
from .lookups import *

from crispy_forms.bootstrap import *
from crispy_forms.helper import *
from crispy_forms.layout import *
from selectable.forms import AutoCompleteWidget

import datetime


class ProductForm(forms.Form):
    autocomplete = forms.CharField(
        label = '',
        widget = AutoCompleteWidget(ProductLookup),
        required = False,
    )

# class ProductForm(forms.ModelForm):
    # Meta = select2_modelform_meta(Product)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(Div(InlineRadios('')),)

    # class Meta:
    #     model = Product
    #     fields = ('name',)

    # metadata = JSONField()
    # product_name = forms.ModelChoiceField(required=True, label="", queryset=Product.objects.all().order_by('name'), widget=Select2(attrs={'class': "search-container"}))
    # product_name = AutoCompleteSelectField('productlookup', required=False, help_text=None)
    # product_name = AutoCompleteSelectMultipleField('name', required=False, help_text=None)
    # ticker_name = forms.CharField(required=False, label=_('Ticker Name:'), widget=forms.TextInput(attrs={'class': "form-control"}))
    # sector = forms.ModelChoiceField(required=True, label="Sector", queryset=MarketSector.objects.all().order_by('title'), widget=Select2(attrs={'class': "form-control"}))
    # board = forms.ModelChoiceField(required=True, label="Board", queryset=MarketBoard.objects.all().order_by('title'), widget=Select2(attrs={'class': "form-control"}))
    # ipo_date = forms.DateField(required=True, label=_("IPO Date:"), widget=DatePickerInput(format="%d-%m-%Y", attrs={'class': "form-control"}))

# class ProductForm(forms.Form):
    # product_name = forms.ModelChoiceField(queryset=Product.objects.all().order_by('name'), widget=Select2())
    # product_name = forms.ModelChoiceField(required=True, label="", queryset=Product.objects.all().order_by('name'), widget=Select2(attrs={'class': "form-control"}))