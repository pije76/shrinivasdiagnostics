from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, TemplateView, View
 
# from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
# from haystack.query import SearchQuerySet

from .models import Category
from .forms import *

from accounts.forms import *

import razorpay
import json

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

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
	user_id = Profile.objects.get(email = request.user)
	user_order = Order.objects.filter(user=user_id, ordered=False).count()
	cart_product_form=CartAddProductForm()

	context = {
		'page_title': page_title,
		'product': product,
		'cart_product_form': cart_product_form,
		'user_order': user_order,
	}

	return render(request, 'shop/product_detail.html', context)


def add_to_cart(request, pk):
	product = get_object_or_404(Product, pk=pk)
	order_item, created = Order.objects.get_or_create(product=product, user=request.user, ordered=False)
	order_qs = Checkout.objects.filter(user=request.user, ordered=False)

	if order_qs.exists():
		order = order_qs[0]

		if order.items.filter(product__pk=product.pk).exists():
			order_item.quantity += 1
			order_item.save()
			messages.info(request, "Added quantity Item")
			return redirect("shopping_cart")
		else:
			order.items.add(order_item)
			messages.info(request, "Item added to your cart")
			return redirect("shopping_cart")
	else:
		checkout_date = timezone.now()
		order = Checkout.objects.create(user=request.user, checkout_date=checkout_date)
		order.items.add(order_item)
		messages.info(request, "Item added to your cart")
		return redirect("shopping_cart")


def remove_from_cart(request, pk):
	product = get_object_or_404(Product, pk=pk)
	order_qs = Checkout.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(product__pk=product.pk).exists():
			order_item = Order.objects.filter(product=product, user=request.user, ordered=False)[0]
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
	product = get_object_or_404(Product, pk=pk)
	order_qs = Checkout.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(product__pk=product.pk).exists():
			order_item = Order.objects.filter(product=product, user=request.user, ordered=False)[0]
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
	user_id = Profile.objects.get(email = request.user)
	user_order = Order.objects.filter(user=user_id, ordered=False).count()
	total_price = request.GET.get('total_price')
	print("total_price:", total_price)
	print('user_order', user_order)

	try:
		cart_order = Checkout.objects.get(user=request.user, ordered=False)
		# product = Product.objects.get(user=request.user, order=False)
		products = Product.objects.filter(available=True)
		product = products.count()
		print('product', product)
		# get_total_item_price = products.price
		# print('get_total_item_price', get_total_item_price)

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


def checkout(request):
	page_title = _('Checkout | ShrinivasDiagnostic')
	user_id = Profile.objects.get(email = request.user)
	patients = Patient.objects.filter(user_patient=user_id)
	user_order = Order.objects.filter(user=user_id, ordered=False).count()
	products = Order.objects.filter(user=user_id)
	cart_order = Checkout.objects.get(user=request.user, ordered=False)
	total_payment = Order.objects.filter(user=request.user)
	payment_mode = request.GET.get('payment_mode')
	total_price = request.GET.get('total_price')
	amount = total_price
	currency = 'INR'

	# form = PatientForm()

	# if request.method == 'POST':

	if payment_mode == "Online":

		# razorpay_order = razorpay_client.order.create({"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"})
		razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
		# print("razorpay_order:", razorpay_order)
		provider_order_id = razorpay_order['id']
		callback_url = 'paymenthandler/'
		# order = Payment.objects.create(user=user_id, amount=amount, provider_order_id=razorpay_order["id"])
		# print("order:", order)
		# order.save()

		print("amount1", amount)

		context = {
			"provider_order_id": provider_order_id,
			"razorpay_merchant_key": settings.RAZORPAY_KEY_ID,
			"callback_url": callback_url,
			"amount": amount,
			"currency": currency,
			"page_title": page_title,
			"user_order": user_order,
			"products": products,
			"total_payment": total_payment,
			"patients": patients,
		}
		return render(request, 'shop/checkout.html', context=context)

	else:
		context = {
			"page_title": page_title,
			"user_order": user_order,
			"products": products,
			"cart_order": cart_order,
			"total_payment": total_payment,
			"patients": patients,
			"amount": amount,
			"currency": currency,
		}
		print("amount2", amount)
		return render(request, 'shop/checkout.html', context=context)

			# order = Payment.objects.create(user=user_id, amount=amount)
			# order.save()

	# 	form = PatientForm(request.POST or None)

	# 	if form.is_valid():
	# 		patient = form.save(commit=False)
	# 		patient.name = form.cleaned_data['name']
	# 		patient.email = form.cleaned_data['email']
	# 		patient.phone_number = form.cleaned_data['phone_number']
	# 		patient.save()

	# 		messages.success(request, _('Your patient profile has been change successfully.'))
	# 		return HttpResponseRedirect('/profile/')
	# 	else:
	# 		messages.warning(request, form.errors)

	# else:
	# 	form = PatientForm()

		# context = {
		# 	"callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/",
		# 	"razorpay_key": settings.RAZORPAY_KEY_ID,
		# 	# "order": order,
		# 	"cart_order": cart_order,
		# 	"page_title": page_title,
		# 	"user_order": user_order,
		# 	"products": products,
		# 	"total_payment": total_payment,
		# 	"patients": patients,
		# }

		# return render(request, "shop/checkout.html", context)

	# context = {
	# 	"page_title": page_title,
	# 	"user_order": user_order,
	# 	"cart_order": cart_order,
	# 	"products": products,
	# 	"total_payment": total_payment,
	# 	"patients": patients,
	# }
	# return render(request, "shop/checkout.html", context)


@csrf_exempt
def callback(request):
	def verify_signature(response_data):
		return razorpay_client.utility.verify_payment_signature(response_data)

	if "razorpay_signature" in request.POST:
		payment_id = request.POST.get("provider_order_id", "")
		provider_order_id = request.POST.get("provider_order_id", "")
		signature_id = request.POST.get("razorpay_signature", "")
		order = Order.objects.get(provider_order_id=provider_order_id)
		order.payment_id = payment_id
		order.signature_id = signature_id
		order.save()

		context = {
			"status": order.status,
		}

		if not verify_signature(request.POST):
			order.status = PaymentStatus.SUCCESS
			order.save()
			return render(request, "shop/callback.html", context)
		else:
			order.status = PaymentStatus.FAILURE
			order.save()
			return render(request, "shop/callback.html", context)
	else:
		payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
		provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
			"id"
		)
		order = Order.objects.get(provider_order_id=provider_order_id)
		order.payment_id = payment_id
		order.status = PaymentStatus.FAILURE
		order.save()

		context = {
			"status": order.status,
		}

		return render(request, "shop/callback.html", context)


#@csrf_exempt
def paymenthandler(request):
	if request.method == "POST":
		try:
			payment_id = request.POST.get('provider_order_id', '')
			provider_order_id = request.POST.get('provider_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'provider_order_id': provider_order_id,
				'provider_order_id': payment_id,
				'razorpay_signature': signature
			}

			result = razorpay_client.utility.verify_payment_signature(params_dict)
			if result is not None:
				total_price = request.GET.get('total_price')
				amount = total_price
				try:
					razorpay_client.payment.capture(payment_id, amount)
					return render(request, 'shop/paymentsuccess.html')
				except:
					return render(request, 'shop/paymentfail.html')
			else:
				return render(request, 'shop/paymentfail.html')
		except:
			return HttpResponseBadRequest()
	else:
		return HttpResponseBadRequest()


def order_payment(request):
	name = Profile.objects.get(email=request.user)
	total_price = request.GET.get('total_price')
	amount = total_price

	if request.method == "POST":
		# razorpay_order = razorpay_client.order.create({"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"})
		razorpay_order = razorpay_client.order.create({"amount": amount, "currency": "INR", "payment_capture": "1"})
		order = Payment.objects.create(user=name, amount=amount, provider_order_id=razorpay_order["id"])
		order.save()

		context = {
			"callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/",
			"razorpay_key": settings.RAZORPAY_KEY_ID,
			"order": order,
		}
		return render(request, "order/checkout.html", context)
	else:
		return render(request, "order/checkout.html")


def my_orders(request):
	context = {
		# 'page_title': page_title,
		# 'form': form,
	}

	return render(request, 'shop/order.html', context)


def create_billingaddress(request):
	form = Add_BillingForm(request.POST or None)

	if request.method == "POST":
		if form.is_valid():
			form.save()
			return redirect ('home')
	context = {
		"form":form
	}
	return render(request, 'app/createform.html', context)


def update_billingaddress(request, id):
	post = get_object_or_404(Post, id=id)
	form = Update_BillingForm(instance=post)

	if request.method == "POST":
		form = Update_BillingForm(request.POST or None, instance=post)

		if form.is_valid():
			post = Post.objects.get(id=1)
			post.title = "update title"
			form.save()

			messages.success(request, _(page_title + ' form was updated.'))
			return render(request, "shop/payment.html", context)
		else:
			messages.warning(request, formset.errors)
	else:
		context = {
			'logos': logos,
			'titles': titles,
			'page_title': page_title,
			'patients': patients,
			'profiles': profiles,
			'icnumbers': icnumbers,
			'formset': formset,
			"themes": themes,
		}

	return render(request, "shop/payment.html", context)


# class CheckoutView(View):
#     def get(self, *args, **kwargs):
#         form = CheckoutForm()
#         context = {
#             'form': form
#         }
#         return render(self.request, 'shop/checkout.html', context)

#     def post(self, *args, **kwargs):
#         form = CheckoutForm(self.request.POST or None)

#         try:
#             order = Order.objects.get(user=self.request.user, ordered=False)
#             if form.is_valid():
#                 street_address = form.cleaned_data.get('street_address')
#                 apartment_address = form.cleaned_data.get('apartment_address')
#                 country = form.cleaned_data.get('country')
#                 zip = form.cleaned_data.get('zip')
#                 same_billing_address = form.cleaned_data.get('same_billing_address')
#                 save_info = form.cleaned_data.get('save_info')
#                 payment_option = form.cleaned_data.get('payment_option')

#                 billing_address = Address(user=self.request.user, street_address=street_address, apartment_address=apartment_address, country=country, zip=zip)
#                 billing_address.save()
#                 order.billing_address = billing_address
#                 order.save()
#                 return redirect('shop:checkout')
#             messages.warning(self.request, "Failed Chekout")
#             return redirect('shop:checkout')

#         except ObjectDoesNotExist:
#             messages.error(self.request, "You do not have an order")
#             return redirect("shopping_cart")

# checkout_view = CheckoutView.as_view()



# class OrderSummaryView(LoginRequiredMixin, View):
#     def get(self, *args, **kwargs):
#         try:
#             order = Order.objects.get(user=self.request.user, ordered=False)
#             context = {
#                 'object' : order,
#             }
#             return render(self.request, 'shop/shopping_cart.html', context)
#         except ObjectDoesNotExist:
#             messages.error(self.request, "You do not have an order")
#             return redirect("/")

# shopping_cart = OrderSummaryView.as_view()


# def autocomplete(request):
#     sqs = SearchQuerySet().autocomplete(
#         title_auto=request.GET.get(
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


