from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.urls import reverse

from .models import *
from .forms import *

from accounts.models import *
from accounts.forms import *

import razorpay
import json

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Create your views here.
def checkout(request):
	page_title = _('Checkout | ShrinivasDiagnostic')
	user_id = Profile.objects.get(email=request.user)
	patients = Patient.objects.filter(user_patient=user_id)
	products = Order.objects.filter(user=user_id)
	user_address = Address.objects.filter(user=user_id)
	user_order = Order.objects.filter(user=user_id).count()
	name = user_id.name
	phone_number = user_id.phone_number
	email = user_id.email

	total_payment = Order.objects.filter(user=user_id)
	cart_order = Checkout.objects.get(user=user_id, ordered=False)

	payment_mode = request.GET.get('payment_mode')
	currency = 'INR'
	store_name = "ShrinivasDiagnostic"
	amount = cart_order.get_total_price
	razorpay_key = settings.RAZORPAY_KEY_ID
	razorpay_order = razorpay_client.order.create({"amount": int(amount) * 100, "currency": currency, "receipt": "1"})
	razorpay_order_id = razorpay_order['id']
	callback_url = 'paymenthandler/'
	# callback_url = "http://" + "127.0.0.1:8000" + "/paymenthandler/",
	data = dict()

	context = {
		"page_title": page_title,
		"user_order": user_order,
		"products": products,
		"cart_order": cart_order,
		"total_payment": total_payment,
		"user_address": user_address,
		"patients": patients,
		"amount": amount,
		"currency": currency,
		"store_name": store_name,
		"name": name,
		"email": email,
		"phone_number": phone_number,
		"razorpay_order_id": razorpay_order_id,
		"razorpay_key": razorpay_key,
		"callback_url": callback_url,
	}

	if request.method == "GET":

		form = PatientForm()
		# form = CheckoutForm(request.POST or None)

		# else:
		# context = {
		#     "page_title": page_title,
		#     "user_order": user_order,
		#     "products": products,
		#     "cart_order": cart_order,
		#     "total_payment": total_payment,
		#     "user_address": user_address,
		#     "patients": patients,
		#     "amount": amount,
		#     "currency": currency,
		#     "store_name": store_name,
		#     "name": name,
		#     "email": email,
		#     "phone_number": phone_number,
		#     "razorpay_order_id": razorpay_order_id,
		#     "razorpay_key": razorpay_key,
		#     "callback_url": callback_url,
		# }
		return render(request, 'checkout/checkout.html', context=context)

	# if request.method == 'POST':
	# if payment_mode == "Online":
	# if request.method == "POST" and payment_mode == "Online" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
	if request.method == "POST" and payment_mode == "Online":
		user_id = Profile.objects.get(email=request.user)
		name = user_id.name
		# amount = request.POST.get('amount')
		amount = request.GET.get('amount')
		currency = 'INR'
		razorpay_key = settings.RAZORPAY_KEY_ID

		print("amount", amount)
		print("payment_mode Online", payment_mode)
		print("POST", request.POST)

		# razorpay_order = razorpay_client.order.create({"amount": int(amount) * 100, "currency": "INR", "receipt": "1"})
		# razorpay_order = razorpay_client.order.create(dict(amount=amount*100, currency=currency, receipt='0'))
		razorpay_order = razorpay_client.order.create({"amount": int(amount) * 100, "currency": currency, "receipt": "1"})
		razorpay_order_id = razorpay_order['id']
		callback_url = 'paymenthandler/'
		# callback_url = "http://" + "127.0.0.1:8000" + "/paymenthandler/",
		order = Payment.objects.create(user=user_id, amount=amount, razorpay_order_id=razorpay_order["id"])
		order.save()

		context = {
			"order": order,
			"razorpay_key": razorpay_key,
			"callback_url": callback_url,
			# "amount": amount,
			# "currency": currency,
		}

		# return JsonResponse(data)
		return render(request, 'checkout/checkout.html', context=context)
	# else:
	#   return JsonResponse({"response error": form.errors}, status=400)

	if request.method == "POST" and payment_mode == "Cash":
		# page_title = _('Checkout | ShrinivasDiagnostic')
		# user_id = Profile.objects.get(email=request.user)
		# user_address = Address.objects.filter(user=user_id)
		# patients = Patient.objects.filter(user_patient=user_id)
		# user_order = Order.objects.filter(user=user_id).count()
		# products = Order.objects.filter(user=user_id)
		# cart_order = Checkout.objects.get(user=request.user, ordered=False)
		# amount = cart_order.get_total_price
		# total_payment = Order.objects.filter(user=request.user)
		# # payment_mode = request.GET.get('payment_mode')
		# currency = 'INR'
		# razorpay_order = razorpay_client.order.create({"amount": int(amount) * 100, "currency": currency, "receipt": "1"})
		# razorpay_order_id = razorpay_order['id']
		# store_name = "ShrinivasDiagnostic"
		# name = user_id.name
		# email = user_id.email
		# phone_number = user_id.phone_number
		# razorpay_key = settings.RAZORPAY_KEY_ID

		# context = {
		#     "page_title": page_title,
		#     "user_order": user_order,
		#     "products": products,
		#     "total_payment": total_payment,
		#     "total_price": total_price,
		#     "patients": patients,
		# }

		# return render(request, 'checkout/thanks.html', context=context)
		return redirect(reverse('my_orders'))

	# return render(request, 'checkout/thanks_cash.html', context=context)
	return redirect(reverse('my_orders'))

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

