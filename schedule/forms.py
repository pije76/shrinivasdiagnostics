from django import forms
from django.forms import ModelForm
from django.forms import widgets
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# from django.contrib.postgres.fields.jsonb import JSONField

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


class ScheduleForm(forms.Form):
    class Meta:
        model = Schedule
        # fields = ('full_name', 'birth_city', 'birth_date')
        fields = '__all__'
        widgets = {
            # 'member': forms.HiddenInput(),
        }

    full_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'required': 'true'}))
    # phone_number = forms.CharField(required=False, label=_('Phone Number:'), widget=forms.TextInput(attrs={'class': "form-control"}))
    # phone_number = PhoneNumberField(region="CA")
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'required': 'true'}))
    # phone_number = PhoneNumberField(region="FR", widget=PhoneNumberPrefixWidget(initial="FR", country_choices=[("CA", "Canada"),("FR", "France"),],),)
    # phone_number = PhoneNumberField(region="FR", widget=PhoneNumberPrefixWidget(initial="FR", country_choices=[("CA", "Canada"),("FR", "France"),],),)
    # phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='GE'))
    city = forms.CharField(required=False, label=_('City:'), widget=forms.TextInput(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(Div(InlineRadios('')),)
