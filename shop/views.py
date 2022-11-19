from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, TemplateView, View

 
# from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
# from haystack.query import SearchQuerySet

from .models import *
from .forms import *

from accounts.models import *
from accounts.forms import *

from checkout.models import *

import json


def product_list(request, category_slug=None):
	page_title = _('Book Blood Test Online in India with Ease with Shrinivas Diagnostics Labs')
	category = None
	categories = Category.objects.all()
	products = Product.objects.filter(available=True)

	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		products = products.filter(category=category)

	context = {
		'page_title': page_title,
		'category': category,
		'categories': categories,
		'products': products,
	}

	return render(request, 'shop/product_list.html', context)


def product_detail(request, pk):
	product = get_object_or_404(Product, id=pk, available=True)
	page_title = product
	user_id = Profile.objects.get(email=request.user)
	user_order = Order.objects.filter(user=user_id).count()
	cart_product_form=CartAddProductForm()

	context = {
		'page_title': page_title,
		'product': product,
		'cart_product_form': cart_product_form,
		'user_order': user_order,
	}

	return render(request, 'shop/product_detail.html', context)


def add_to_cart(request, pk):
	item = get_object_or_404(Product, pk=pk)
	order_item, created = Order.objects.get_or_create(product=item, user = request.user, ordered = False)
	order_qs = Checkout.objects.filter(user=request.user, ordered= False)

	if order_qs.exists():
		order = order_qs[0]

		if order.items.filter(product__pk=item.pk).exists():
			order_item.quantity += 1
			order_item.save()
			messages.info(request, "Added quantity Item")
			return redirect("shopping_cart")
		else:
			order.items.add(order_item)
			messages.info(request, "Item added to your cart")
			return redirect("shopping_cart")
	else:
		ordered_date = timezone.now()
		order = Checkout.objects.create(user=request.user, ordered_date=ordered_date)
		order.items.add(order_item)
		messages.info(request, "Item added to your cart")
		return redirect("shopping_cart")


def remove_from_cart(request, pk):
	item = get_object_or_404(Product, pk=pk)
	order_qs = Checkout.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(product__pk=item.pk).exists():
			order_item = Order.objects.filter(product=item, user=request.user, ordered=False)[0]
			order_item.delete()
			messages.info(request, "Item \""+order_item.product.product_name+"\" remove from your cart")
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
			order_item = Order.objects.filter(product=item, user=request.user, ordered=False)[0]
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


def shopping_cart(request):
	page_title = _('Cart | ShrinivasDiagnostic')
	user_id = Profile.objects.get(email=request.user)
	user_order = Order.objects.filter(user=user_id).count()
	total_price = request.GET.get('total_price')

	try:
		cart_order = Checkout.objects.get(user=request.user, ordered=False)
		# product = Product.objects.get(user=request.user, order=False)
		products = Product.objects.filter(available=True)
		product = products.count()
		# get_total_item_price = products.price

		context = {
			'cart_order': cart_order,
			'products': products,
			'user_order': user_order,
			'page_title': page_title,
		}
		return render(request, 'shop/shopping_cart.html', context)
	except ObjectDoesNotExist:
		messages.error(request, "You do not have an order")
		return redirect("/")


# def autocomplete(request):
#     sqs = SearchQuerySet().autocomplete(
#         content_auto=request.GET.get(
#             'query',
#             ''))[
#         :5]
#     s = []
#     for result in sqs:
#         d = {"value": result.title, "data": result.object.slug}
#         s.append(d)
#     output = {'suggestions': s}
#     return JsonResponse(output)


# class FacetedSearchView(BaseFacetedSearchView):

#     form_class = FacetedProductSearchForm
#     facet_fields = ['category', 'brand']
#     template_name = 'shop/product/product_search.html'
#     paginate_by = 3
#     context_object_name = 'object_list'


