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

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Create your views here.
def checkout(request):
	page_title = _('Checkout | ShrinivasDiagnostic')
	user_id = Profile.objects.get(email=request.user)
	patients = Patient.objects.filter(user_patient=user_id)
	products = Order.objects.filter(user=user_id)
	user_address = Address.objects.filter(user=user_id)
	user_order = Order.objects.filter(user=user_id, item_order=False).count()
	# client_orders = Order.objects.filter(user=user_id, item_order=False)
	full_name = user_id.full_name
	phone_number = user_id.phone_number
	email = user_id.email

	total_payment = Order.objects.filter(user=user_id)
	try:
		cart_order = Checkout.objects.get(user=user_id, ordered=False)
	except ObjectDoesNotExist:
		messages.error(request, "You do not have an order")
		return redirect("shop:product_list")
	payment_mode = request.POST.get('payment_mode')

	currency = 'INR'
	amount = cart_order.get_total_price
	amount = float(amount)
	razorpay_key = settings.RAZORPAY_KEY_ID
	# callback_url = 'checkout/callback/'
	# callback_url = 'paymenthandler/'
	# callback_url = "http://" + "127.0.0.1:8000" + "/paymenthandler/",
	store_name = "ShrinivasDiagnostic"

	if request.method == 'POST':
		if request.POST.get('payment_mode') == 'Online':
			razorpay_order = client.order.create({"amount": int(amount) * 100, "currency": currency, "payment_capture": "1"})
			provider_order_id = razorpay_order['id']
			order = Checkout.objects.update(user=user_id, amount=amount, provider_order_id=provider_order_id)
			# order.save()

			context = {
				"razorpay_key": razorpay_key,
				"provider_order_id": provider_order_id,
				"order": order,
				# "callback_url": callback_url,
				"amount": amount,
				"currency": currency,
				"phone_number": phone_number,
				"email": email,
				"full_name": full_name,
				"store_name": store_name,
			}
			# return render(request, 'checkout/checkout.html', context=context)
			return render(request, 'checkout/payment.html', context=context)

		else:

	# 	if request.POST.get('payment_mode') == 'Cash':
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
	# 	form = OrderForm(instance=request.user)
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

		}

	return render(request, 'checkout/checkout.html', context=context)

	# # time.sleep(5)
	# # return redirect(reverse('my_orders'))
	# # return render(request, 'checkout/checkout.html', context=context)
	# return render(request, 'checkout/checkout.html')


@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "checkout/callback.html", context={"status": order.status})
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "checkout/callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "checkout/callback.html", context={"status": order.status})

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
			payment_id = request.POST.get('provider_order_id', '')
			provider_order_id = request.POST.get('provider_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'provider_order_id': provider_order_id,
				'provider_order_id': payment_id,
				'razorpay_signature': signature
			}

			result = client.utility.verify_payment_signature(params_dict)

			if result is not None:
				amount = 20000
				try:
					client.payment.capture(payment_id, amount)
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

