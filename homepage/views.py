from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from .models import *
from .forms import *

from accounts.models import *
from shop.models import *
from shop.forms import *
from order.models import *
from schedule.forms import *

from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView, SearchView
from haystack.query import SearchQuerySet

# Create your views here.
def index(request):
	is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
	page_title = _('Check the Best Blood Test &amp; Pathology Lab in India with Shrinivas Diagnostics Labs')
	user_id = request.user.is_authenticated
	user_order = Order.objects.filter(user=user_id, item_order=False).count()
	products = Product.objects.filter(available=True)

	initial_dict = {
		# 'ticker_code': get_ticker_id,
	}

	aforms = ProductForm()
	bforms = ScheduleForm()

	if request.method == "POST":
		aforms = ProductForm(request.POST or None)
		bforms = ScheduleForm(request.POST or None)

		# if aforms.is_valid() and bforms.is_valid():
		if bforms.is_valid():
			# products = Schedule()
			# # products.title = aforms.cleaned_data['title']
			# products.title = aforms.cleaned_data['title']
			# # products = aforms.cleaned_data['duration_time_from']
			# products.phone_number = aforms.cleaned_data['phone_number']
			# products.city = aforms.cleaned_data['city']
			# # products = Schedule()
			# products.save()

			schedule = Schedule()
			schedule.full_name = bforms.cleaned_data['full_name']
			schedule.phone_number = bforms.cleaned_data['phone_number']
			schedule.city = bforms.cleaned_data['city']
			schedule.save()

			# messages.success(request, 'aforms was created.')
			messages.success(request, 'Your Home Collection Schedule was created.')
			return redirect('homepage:index')
		else:
			# messages.warning(request, aforms.errors)
			messages.warning(request, bforms.errors)
	else:
		# aforms = ProductForm(initial=initial_dict)
		# bforms = ScheduleForm(initial=initial_dict)

		context = {
			'page_title': page_title,
			'user_order': user_order,
			'products': products,
			'aforms': aforms,
			'bforms': bforms,
		}
		return render(request, 'homepage/home.html', context)

def productlist_search(request):
	results = None

	if request.method == "GET":
		if "q" in request.GET:
			query = str(request.GET.get("q"))
			# Add extra code here to parse the "content" query string parameter...
			# * Get content type to search for
			# content_type = request.GET.get("content")
			# * Assign the model or models to a list for the "models" call
			search_models = []
			search_models = [Product]
			# * Add a "models" call to limit the search results to the particular models
			results = SearchQuerySet().all().filter(q=query).models(*search_models)

			context = {
				'results': results,
			}
	return render(request, "shop/product_list.html", context)
