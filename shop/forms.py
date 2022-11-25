from django import forms

from .models import *
from accounts.models import *
from address.models import *

from haystack.forms import FacetedSearchForm, SearchForm
from haystack.inputs import Exact

from crispy_forms.bootstrap import *
from crispy_forms.helper import *
from crispy_forms.layout import *

# from easy_select2 import *

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

class ProductFindForm(forms.ModelForm):
	# Meta = select2_modelform_meta(Product)

	class Meta:
		model = Product
		# fields = ('title')
		fields = '__all__'
		widgets = {
			# "title": MarketWidget,
			# "title": apply_select2(forms.Select),
		}

	# title = forms.ModelChoiceField(required=True, label="", queryset=Product.objects.all().order_by('available'), widget=Select2(attrs={'class': "test_search_input_field search__test_package box"}))
	# longitude = forms.ModelChoiceField(label=u"City", queryset=City.objects.all(), widget=ModelSelect2Widget(model=City, search_fields=['longitude__icontains'], dependent_fields={'city': 'city'}, max_results=500,))
	# aspect = forms.MultipleChoiceField(required=False, label="Aspect: ", widget=forms.CheckboxSelectMultiple(attrs={'class': "form-control"}), choices=ASPECT_GEOMETRY_CHOICES)

	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	self.helper = FormHelper()
	# 	self.helper.layout = Layout(Div(InlineRadios('')),)


class ProductSearchForm(SearchForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 Main St'}))

	def search(self):
		# First, store the SearchQuerySet received from other processing.
		sqs = super().search()

		if not self.is_valid():
			return self.no_query_found()

		if self.cleaned_data['title']:
			# sqs = sqs.filter(available=True)
			sqs = sqs.filter(available=self.cleaned_data['title'])

		return sqs

class FacetedProductSearchForm(FacetedSearchForm):

	def __init__(self, *args, **kwargs):
		data = dict(kwargs.get("data", []))
		self.title = data.get('title', [])
		super(FacetedProductSearchForm, self).__init__(*args, **kwargs)

	def search(self):
		sqs = super(FacetedProductSearchForm, self).search()

		if self.title:
			query = None
			for title in self.title:
				if query:
					query += u' OR '
				else:
					query = u''
				query += u'"%s"' % sqs.query.clean(title)
			sqs = sqs.narrow(u'title_exact:%s' % query)
		return sqs
