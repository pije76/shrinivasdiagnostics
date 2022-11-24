from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, TemplateView, View

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response

from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView, SearchView
from haystack.query import SearchQuerySet

from .models import *
from .forms import *

from accounts.models import *
from accounts.forms import *

from order.models import *

# import json
import simplejson as json

def productlist_search(request):
	sqs = None

	if request.method == "GET":
		if "q" in request.GET:
			query = str(request.GET.get("q"))
			search_models = []
			search_models = [Product]
			sqs = SearchQuerySet().all().filter(q=query).models(*search_models)
			# sqs = SearchQuerySet().autocomplete(title_auto=query).models(*search_models)
			# suggestions = [result.title for result in sqs]
			# suggestions = [{'text':result.title, 'url':generate_url(result), }
			# 	for result in sqs
			# ]

			# the_data = json.dumps(
			# {
			# 	'sqs': suggestions,
				# 'query': query
				# 'sqs': sqs
			# })

			context = {
				'sqs': sqs,
			}

			# return JsonResponse({'sqs': suggestions})
	return render(request, "shop/product_list.html", context)
	# return HttpResponse(the_data, content_type='application/json')
	# return HttpResponse(the_data, mimetype='application/json')
	# return JsonResponse(the_data, safe=False)
	# return JsonResponse({'sqs': suggestions})

# @api_view(['POST'])
# def productlist_search(request):
# 	name = request.data['name']
# 	customer = SearchQuerySet().models(Customer).autocomplete(first_name__startswith=name)

# 	searched_data = []
# 	for i in customer:
# 		all_results = {"first_name": i.first_name, "last_name": i.last_name, "balance": i.balance, "status": i.customer_status,}
# 		searched_data.append(all_results)

# 	return Response(searched_data)

def product_list(request, category_slug=None):
	page_title = _('Book Blood Test Online in India with Ease with Shrinivas Diagnostics Labs')
	category = None
	categories = Category.objects.all()
	object_list = Product.objects.filter(available=True)
	user_id = request.user.is_authenticated
	user_order = Order.objects.filter(user=user_id, item_order=False).count()

	is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		object_list = object_list.filter(category=category)

	if request.method == "GET":
	# if request.method == "GET" and is_ajax:
		form = ProductFindForm()

		if form.is_valid():
			# save_geoastro.natalstock_pluto = get_geo_pluto(get_tz)
			# save_geoastro.save()

			messages.warning(request, "Sukses")
			# return redirect('core:homepage')
			return render(request, 'shop/product_list.html', context)
		else:
			messages.warning(request, form.errors)


	context = {
		'page_title': page_title,
		'category': category,
		'categories': categories,
		'object_list': object_list,
		'user_order': user_order,
		'form': form,
		# 'sqs': sqs,
	}

	return render(request, 'shop/product_list.html', context)



def product_detail(request, pk):
	product = get_object_or_404(Product, id=pk, available=True)
	page_title = product
	user_id = Profile.objects.get(email=request.user)
	user_order = Order.objects.filter(user=user_id, item_order=False).count()
	cart_product_form=CartAddProductForm()

	context = {
		'page_title': page_title,
		'product': product,
		'cart_product_form': cart_product_form,
		'user_order': user_order,
	}

	return render(request, 'shop/product_detail.html', context)


@login_required(login_url='/')

def shopping_cart(request):
	page_title = _('Cart | ShrinivasDiagnostic')
	user_id = Profile.objects.get(email=request.user)
	user_order = Order.objects.filter(user=user_id, item_order=False).count()
	total_price = request.GET.get('total_price')

	try:
		cart_order = Checkout.objects.get(user=request.user, ordered=False)
		# product = Product.objects.get(user=request.user, order=False)
		products = Product.objects.filter(available=True)
		product = products.count()
		# get_total_item_price = products.price

		if user_order == 0:
			display_result = True
		else:
			display_result = False

		context = {
			'cart_order': cart_order,
			'products': products,
			'user_order': user_order,
			'page_title': page_title,
			'display_result': display_result,
		}
		return render(request, 'shop/shopping_cart.html', context)
	except ObjectDoesNotExist:
		messages.error(request, "You do not have an order")
		return redirect("shop:product_list")


def add_to_cart(request, pk):
	item = get_object_or_404(Product, pk=pk)
	order_item, created = Order.objects.get_or_create(product=item, user=request.user, item_order=False)
	order_qs = Checkout.objects.filter(user=request.user, ordered=False)

	if order_qs.exists():
		order = order_qs[0]

		if order.items.filter(product__pk=item.pk).exists():
			order_item.quantity += 1
			order_item.save()
			messages.info(request, "Added quantity Item")
			return redirect("shopping_cart")
		else:
			order.items.add(order_item)
			messages.info(request, "Item \""+order_item.product.title+"\" added to your cart")
			return redirect("shopping_cart")
	else:
		checkout_date = timezone.now()
		order = Checkout.objects.create(user=request.user, checkout_date=checkout_date)
		order.items.add(order_item)
		messages.info(request, "Item \""+order_item.product.title+"\" added to your cart")
		return redirect("shopping_cart")


def remove_from_cart(request, pk):
	item = get_object_or_404(Product, pk=pk)
	order_qs = Checkout.objects.filter(user=request.user, ordered=False)

	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(product__pk=item.pk).exists():
			order_item = Order.objects.filter(product=item, user=request.user, item_order=False)[0]
			order_item.delete()
			messages.info(request, "Item \""+order_item.product.title+"\" remove from your cart")
			return redirect("shopping_cart")
		else:
			messages.info(request, "This Item not in your cart")
			return redirect("shopping_cart")
	else:
		messages.info(request, "You do not have an Order")
		return redirect("shopping_cart")


def reduce_quantity_item(request, pk):
	item = get_object_or_404(Product, pk=pk)
	order_qs = Checkout.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(product__pk=item.pk).exists():
			order_item = Order.objects.filter(product=item, user=request.user, item_order=False)[0]
			if order_item.quantity > 1:
				order_item.quantity -= 1
				order_item.save()
			else:
				order_item.delete()
				messages.info(request, "Item quantity was updated")
			return redirect("shopping_cart")
		else:
			messages.info(request, "This Item not in your cart")
			return redirect("shopping_cart")
	else:
		messages.info(request, "You do not have an Order")
		return redirect("shopping_cart")

def get_add_to_cart_url(request, pk):
	return reverse("shop:add_to_cart", pk=pk)


def autocomplete(request):
	sqs = SearchQuerySet().autocomplete(title_auto=request.GET.get('q', ''))[:5]
	# sqs = SearchQuerySet().autocomplete(title_auto='q')
	# sqs = SearchQuerySet().filter(title_auto=request.GET.get('q', ''))
	# sqs = SearchQuerySet().autocomplete(title_auto=request.POST.get('q', ''))
	# sqs = SearchQuerySet().filter(title_auto=request.GET.get('q', ''))
	# sqs = SearchQuerySet().models(Product).autocomplete(title_auto=request.GET.get('q', ''))
	# sqs = SearchQuerySet().filter(title_auto=request.GET.get('q', ''))
	# sqs = SearchQuerySet().autocomplete(title_auto=request.GET.get('q', ''))

	# s = []
	# for result in sqs:
	# 	d = {"value": result.title, "data": result.object.slug}
	# 	s.append(d)
	# output = {'suggestions': s}

	suggestions = [result.title for result in sqs]
	# Make sure you return a JSON object, not a bare list.
	# Otherwise, you could be vulnerable to an XSS attack.
	the_data = json.dumps(
	{
		'results': suggestions
	})
	# return JsonResponse(output)
	return HttpResponse(the_data, content_type='application/json')


class FacetedSearchView(BaseFacetedSearchView):

	form_class = ProductSearchForm
	facet_fields = ['title']
	template_name = 'shop/product_list.html'
	paginate_by = 3
	context_object_name = 'object_list'


