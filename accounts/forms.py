from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm, HiddenInput
from django.http import Http404
from django.utils.translation import gettext_lazy as _

# from allauth.account.forms import LoginForm, SignupForm
# from bootstrap_datepicker_plus import *
from bootstrap_modal_forms.forms import *
# from bootstrap_modal_forms.mixins import *
# from cities_light.models import *
# from crispy_forms.bootstrap import *
# from crispy_forms.helper import *
# from crispy_forms.layout import *
# from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV2Checkbox, ReCaptchaBase, ReCaptchaV3


from datetime import datetime, date

from .models import *
# from .lookups import *
# from subscription.models import *

# from easy_select2 import *


def get_today():
    return date.today().strftime('%d-%m-%Y')

# class MyLoginForm(BSModalModelForm):
class MyLoginForm(AuthenticationForm):
# class MyLoginForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        model = Profile
        # model = User
        fields = ['phone_number']
        # fields = '__all__'
        
    phone_number = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={'class': "form-control"}))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        # widgets = {
        #     'phone_verified': forms.HiddenInput(),
        # }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        # self.helper = FormHelper()
        # self.helper.layout = Layout(
        #     Div(InlineRadios('')),
        # )

    # full_name = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={'class': "form-control"}))
    # username = forms.CharField(required=False, label="", widget=forms.HiddenInput(attrs={'class': "form-control"}))
    # is_patient = forms.BooleanField(required=False, label='', widget=forms.HiddenInput())
    # is_active = forms.BooleanField(required=False, label='', widget=forms.HiddenInput())
    # email = forms.EmailField(required=False, label="", widget=forms.HiddenInput(attrs={'class': "form-control"}))
    # password = forms.CharField(required=False, label="", widget=forms.HiddenInput(attrs={'class': "form-control"}))
    # address = forms.CharField(required=False, label="", widget=forms.Textarea(attrs={'class': "form-control", 'rows': 4, 'cols': 15}))

