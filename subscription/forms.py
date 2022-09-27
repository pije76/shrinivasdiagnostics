from django import forms
from django.forms import ModelForm, HiddenInput
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings

from bootstrap_datepicker_plus import *
# from django_select2.forms import *
from crispy_forms.bootstrap import *
from crispy_forms.helper import *
from crispy_forms.layout import *

import datetime

from .models import *
# from .widgets import CheckboxSelectMultipleWithSelectAll
# from .lookups import *

# from selectable.forms import AutoCompleteWidget
from easy_select2 import *


class PlanForm(forms.ModelForm):
	class Meta:
		model = Subscription
		# fields = ('ticker_code', 'ipo_date')
		fields = '__all__'
		widgets = {
		#     "ticker_code": MarketWidget,
			'member': forms.HiddenInput(),
			'subscription': forms.HiddenInput(),
			'begin_date': forms.HiddenInput(),
			'expired_date': forms.HiddenInput(),
			'active': forms.HiddenInput(),
			'status': forms.HiddenInput(),
		}

	# member = forms.ChoiceField(required=True, label="", widget=HiddenInput(attrs={'class': "form-control"}))
	# subscription = forms.ChoiceField(required=True, label="", widget=HiddenInput(attrs={'class': "form-control"}))
	# ticker = forms.ChoiceField(required=True, label="", widget=HiddenInput(attrs={'class': "form-control"}))
	# indicator = forms.ChoiceField(required=True, label="", widget=HiddenInput(attrs={'class': "form-control"}))
	# begin_date = forms.ChoiceField(required=True, label="", widget=HiddenInput(attrs={'class': "form-control"}))
	# expired_date = forms.ChoiceField(required=True, label="", widget=HiddenInput(attrs={'class': "form-control"}))
	# expired_date = forms.DateField(required=False, label="", widget=HiddenInput())
	# expired_date = forms.DateField(required=False, label="", widget=DatePickerInput(format="%d-%m-%Y", attrs={'class': "form-control"}))
	# active = forms.ChoiceField(required=True, label="", widget=HiddenInput(attrs={'class': "form-control"}))
	# price = forms.ChoiceField(required=True, label="", widget=HiddenInput(attrs={'class': "form-control"}))
	# quantity = forms.ChoiceField(required=True, label="", widget=HiddenInput(attrs={'class': "form-control"}))
	# status = forms.ChoiceField(required=True, label="", widget=HiddenInput(attrs={'class': "form-control"}))

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(Div(InlineRadios('')),)
		# self.helper.layout = Layout(Field('subscription', type="hidden"))


class IndicatorForm(forms.Form):
	indicator = forms.ChoiceField(required=False, label=_("Indicator"), choices=INDICATOR_CHOICES, widget=forms.Select(attrs={'class': "form-control"}))
