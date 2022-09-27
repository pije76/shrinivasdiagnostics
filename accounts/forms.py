from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm, HiddenInput
from django.http import Http404
from django.utils.translation import gettext_lazy as _

# from allauth.account.forms import LoginForm, SignupForm
# from bootstrap_datepicker_plus import *
# from bootstrap_modal_forms.forms import *
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
        # model = MemberProfile
        model = User
        fields = ['username', 'password']
        # fields = '__all__'
