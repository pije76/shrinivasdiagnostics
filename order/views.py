from django.contrib import messages
from django.shortcuts import redirect, render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import *

from accounts.models import *
from accounts.forms import *

import razorpay
import json
import time

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Create your views here.
def checkout(request):
	page_title = _('Checkout | ShrinivasDiagnostic')
	user_id = Profile.objects.get(email=request.user)
	patients = Patient.objects.filter(user_patient=user_id)
	products = Order.objects.filter(user=user_id)
	user_address = Address.objects.filter(user=user_id)
	user_order = Order.objects.filter(user=user_id, item_order=False).count()
	# client_orders = Order.objects.filter(user=user_id, order=False)
	full_name = user_id.full_name
	phone_number = user_id.phone_number
	email = user_id.email

	total_payment = Order.objects.filter(user=user_id)
	try:
		cart_order = Checkout.objects.get(user=user_id, ordered=False)
	except ObjectDoesNotExist:
		messages.error(request, "You do not have an order")
		return redirect("shop:product_list")
	payment_mode = request.GET.get('payment_mode')

	currency = 'INR'
	amount = cart_order.get_total_price
	razorpay_key = settings.RAZORPAY_KEY_ID
	razorpay_order = razorpay_client.order.create({"amount": int(amount) * 100, "currency": currency, "receipt": "1"})
	razorpay_order_id = razorpay_order['id']
	callback_url = 'callback/'
	# callback_url = 'paymenthandler/'
	# callback_url = "http://" + "127.0.0.1:8000" + "/paymenthandler/",
	store_name = "ShrinivasDiagnostic"
	data = dict()

	if request.method == 'POST':
		form = OrderForm(request.POST or None, instance=request.user)
		payment_mode = request.POST.get('payment_mode')

		if request.POST.get('payment_mode') == 'Online':
			# razorpay_order = razorpay_client.order.create({"amount": int(amount) * 100, "currency": currency, "receipt": "1"})
			# razorpay_order_id = razorpay_order['id']
			# client_payment = Checkout.objects.create(user=user_id, amount=amount, razorpay_order_id=razorpay_order["id"])
			# client_payment.save()

			context = {
				"razorpay_key": razorpay_key,
				"razorpay_order_id": razorpay_order_id,
				# "callback_url": callback_url,
			}
		# return render(request, 'checkout/checkout.html', context=context)

		if request.POST.get('payment_mode') == 'Cash':
			order = Order.objects.filter(user=user_id)
			order.update(item_order=True)
			for object in order:
				object.save()
			checkout = Checkout.objects.filter(user=user_id)
			checkout.update(status="waiting")
			checkout.update(amount=amount)
			for object in checkout:
				object.save()
			return redirect(reverse('my_orders'))

	else:
		form = OrderForm(instance=request.user)
		# return render(request, 'checkout/checkout.html', context=context)
		# return redirect(reverse('my_orders'))

	context = {
		"page_title": page_title,
		"user_order": user_order,
		"products": products,
		"cart_order": cart_order,
		"total_payment": total_payment,
		"user_address": user_address,
		"patients": patients,

		"razorpay_order_id": razorpay_order_id,
		"razorpay_key": razorpay_key,
		"amount": amount,
		"currency": currency,
		# "callback_url": callback_url,
		"store_name": store_name,
		"full_name": full_name,
		"email": email,
		"phone_number": phone_number,
	}

	# time.sleep(5)
	# return redirect(reverse('my_orders'))
	return render(request, 'checkout/checkout.html', context=context)


@csrf_exempt
def callback(request):

	def verify_signature(response_data):
		return razorpay_client.utility.verify_payment_signature(response_data)

	if "razorpay_signature" in request.POST:
		payment_id = request.POST.get("razorpay_payment_id", "")
		razorpay_order_id = request.POST.get("razorpay_order_id", "")
		signature_id = request.POST.get("razorpay_signature", "")
		order = Payment.objects.get(razorpay_order_id=razorpay_order_id)
		order.payment_id = payment_id
		order.signature_id = signature_id
		order.save()

		context = {
			"status": order.status,
		}

		if not verify_signature(request.POST):
			order.status = PaymentStatus.SUCCESS
			order.save()
			return render(request, "checkout/callback.html", context)
		else:
			order.status = PaymentStatus.FAILURE
			order.save()
			return render(request, "checkout/callback.html", context)
	else:
		payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
		razorpay_order_id = json.loads(request.POST.get("error[metadata]")).get("order_id")
		order = Order.objects.get(razorpay_order_id=razorpay_order_id)
		order.payment_id = payment_id
		order.status = PaymentStatus.FAILURE
		order.save()

		context = {
			"status": order.status,
		}

		return render(request, "checkout/callback.html", context)


def my_orders(request):
	page_title = _('My Orders')
	user_id = Profile.objects.get(email=request.user)
	user_order = Order.objects.filter(user=user_id, item_order=False).count()
	user_checkout = Checkout.objects.filter(user=user_id, status="success")
	total_order = Order.objects.filter(user=user_id, item_order=True).count()

	context = {
		'page_title': page_title,
		'user_id': user_id,
		'user_order': user_order,
		'user_checkout': user_checkout,
		'total_order': total_order,
	}

	return render(request, 'accounts/myorder.html', context)



@csrf_exempt
def paymenthandler(request):

	if request.method == "POST":
		try:
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			result = razorpay_client.utility.verify_payment_signature(params_dict)

			if result is not None:
				amount = 20000
				try:
					razorpay_client.payment.capture(payment_id, amount)
					return render(request, 'checkout/paymentsuccess.html')
				except:
					return render(request, 'checkout/paymentfail.html')
			else:
				return render(request, 'checkout/paymentfail.html')
		except:
			return HttpResponseBadRequest()
	else:
		return HttpResponseBadRequest()
		# return render(request, 'paymentfail.html')


def create_billingaddress(request):
	form = Add_BillingForm(request.POST or None)

	if request.method == "POST":
		if form.is_valid():
			form.save()
			return redirect ('home')
	context = {
		"form":form
	}
	return render(request, 'checkout/createform.html', context)


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
			return render(request, "checkout/payment.html", context)
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

	return render(request, "checkout/payment.html", context)

