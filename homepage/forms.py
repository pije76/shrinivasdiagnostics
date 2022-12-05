from django import forms
from django.forms import ModelForm
from django.forms import widgets
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# from django.contrib.postgres.fields.jsonb import JSONField

from shop.models import *
from .models import *

from crispy_forms.bootstrap import *
from crispy_forms.helper import *
from crispy_forms.layout import *
# from selectable.forms import *
# from selectable_select2.widgets import *
# from phonenumber_field.formfields import *
from phonenumber_field.widgets import *
# from django_select2 import forms as s2forms
# from django_select2.forms import *

import datetime

# class ProductWidget(s2forms.Select2Widget):
#     search_fields = [
#         "title__icontains",
#     ]

class ProductForm(forms.Form):
    # autocomplete = forms.CharField(
    #     label = '',
    #     widget = AutoCompleteWidget(ProductLookup),
    #     required = False,
    # )
    # product_title = AutoCompleteSelectField(lookup_class=ProductLookup, label='Select a fruit')
    # product_title = forms.CharField(widget=ProductWidget)
    # product_title = forms.CharField(widget=ModelSelect2Widget(model=Product, search_fields=['title__icontains'])
    product_title = forms.CharField(required=False, widget=forms.TextInput())
    # product_title = AutoCompleteWidget(ProductLookup, placeholder='select related item')
    # product_title = forms.ModelChoiceField(queryset=Product.objects.all().order_by('title'), widget=Select2())
    # product_title = forms.ModelChoiceField(required=True, label="", queryset=Product.objects.all().order_by('title'), widget=Select2(attrs={'class': "form-control"}))

# class ProductForm(forms.ModelForm):
    # Meta = select2_modelform_meta(Product)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(Div(InlineRadios('')),)

    # class Meta:
    #     model = Product
    #     fields = ('title',)
    #     widgets = {
    #         "title": ProductWidget,
    #         # 'title' : AutoCompleteSelect2Widget(ProductLookup, placeholder='Search for a test, health package or Labs')
    #     }

    # metadata = JSONField()
    # product_title = forms.ModelChoiceField(required=True, label="", queryset=Product.objects.all().order_by('title'), widget=Select2(attrs={'class': "search-container"}))
    # product_title = forms.ModelChoiceField(label="", queryset=Product.objects.distinct('scenarioAreaName'), empty_label="Placeholder")

    # product_title = AutoCompleteSelectField('productlookup', required=False, help_text=None)
    # product_title = AutoCompleteSelectMultipleField('title', required=False, help_text=None)

