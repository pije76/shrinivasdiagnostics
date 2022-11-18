from django.conf import settings
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from accounts.models import *
from shop.models import *
from .models import *
from .forms import *

import razorpay
# razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZORPAY_SECRET_KEY))

# Create your views here.
def homepage(request):
	is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
	page_title = _('Check the Best Blood Test &amp; Pathology Lab in India with Shrinivas Diagnostics Labs')
	user_id = request.user.is_authenticated
	user_order = Order.objects.filter(user=user_id).count()
	# member = Profile.objects.get(email=request.user)
	# get_status = Profile.objects.filter(email=request.user).values_list('is_active', flat=True).first()
	# currency = 'INR'
	# amount = 20000
	# razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))

	# order id of newly created order.
	# razorpay_order_id = razorpay_order['id']
	# callback_url = 'paymenthandler/'

	initial_dict = {
		# 'ticker_code': get_ticker_id,
	}
	
	form = ScheduleForm(initial=initial_dict)

	if request.method == "POST":
		form = ScheduleForm(request.POST or None)

		if form.is_valid():
			schedule = Schedule()
			schedule.name = form.cleaned_data['name']
			schedule.phone_number = form.cleaned_data['phone_number']
			schedule.city = form.cleaned_data['city']
			schedule.save()

			messages.success(request, _(page_title + ' form was created.'))
			return redirect('core:homepage')
		else:
			messages.warning(request, form.errors)
	else:
		form = ScheduleForm(initial=initial_dict)

	context = {
		# 'razorpay_order_id': razorpay_order_id,
		# 'razorpay_merchant_key': settings.RAZOR_KEY_ID,
		# 'razorpay_amount': amount,
		# 'currency': currency,
		# 'callback_url': callback_url,
		'form': form,
		'page_title': page_title,
		# 'form': form,
		'user_order': user_order,
	}
	return render(request, 'core/home.html', context)


# def schedule(request):
# 	product = get_object_or_404(Product, id=pk, available=True)

# 	initial_dict = {
# 		# 'ticker_code': get_ticker_id,
# 	}

# 	if request.method == 'POST':
#         form = ScheduleForm(request.POST or None)

#         if form.is_valid():
#             schedule = Schedule()
#             schedule.name = name
#             schedule.phone_number = phone_number
#             schedule.city = city
#             schedule.save()

#             messages.success(request, _(page_title + ' form was created.'))
#             return redirect('core:homepage)
#         else:
#             messages.warning(request, form.errors)

#     else:
#         form = ScheduleForm(initial=initial)

#     context = {
#         'logos': logos,
#         'titles': titles,
#         'page_title': page_title,
#         'patients': patients,
#         'profiles': profiles,
#         'icnumbers': icnumbers,
#         'form': form,
#         "themes": themes,
#     }

#     return render(request, 'core/home.html', context)


# 	context = {
# 		'product': product,
# 	}

# 	return render(request,'header.html')
