from django.shortcuts import render
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from accounts.models import *
from shop.models import *
from .models import *
from .forms import *

# Create your views here.
def homepage(request):
	is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
	titles = _('Check the Best Blood Test &amp; Pathology Lab in India with Shrinivas Diagnostics Labs')
	member = Profile.objects.get(email=request.user)
	get_status = Profile.objects.filter(email=request.user).values_list('is_active', flat=True).first()

	print("get_status", get_status)
	
	initial_dict = {
		# 'ticker_code': get_ticker_id,
	}
	
	form = ProductForm(initial=initial_dict)
	
	# if is_ajax:
	# 	get_board_id = request.GET.get('get_board_id')
	# 	get_ticker_code = MarketDetail.objects.filter(id=get_ticker_id).values_list('ticker_code', flat=True).first()
	# 	cache.set('get_board_id', get_board_id, 30)

	# 	get_ticker_id = cache.get('get_ticker_id')

	# 	context = {
	# 		'titles': titles,
	# 		'get_qs': get_qs,
	# 		'get_ticker_id': get_ticker_id,
	# 		'get_sector_id': get_sector_id,
	# 		'get_board_id': get_board_id,
	# 	}
	# 	return JsonResponse(context)

	# if request.method == "POST":
	# 	form = ProductForm(request.POST or None)
	# 	get_ticker_id = request.POST.get('get_ticker_id')
	# 	cache.set('get_ticker_id', get_ticker_id, 30)
	# 	get_ticker_id = cache.get('get_ticker_id')

	# 	context = {
	# 		'titles': titles,
	# 		# 'form': form,
	# 		# 'chart': dump,
	# 		# 'get_ticker_name': get_ticker_name,
	# 		'get_ticker_name': json.dumps(get_ticker_name),
	# 	}
	# 	return render(request, 'chart/index.html', context)
	# else:
	# 	if get_status == "expired":
	# 		messages.warning(request, "You're Package is expired. Please choose the package to continue.")
	# 		return redirect('subscription:subscription')
	# 	else:
	# 		form = ProductForm(initial=initial_dict, instance=request.user)

	context = {
		'titles': titles,
		'form': form,
		# 'get_ticker_name': get_ticker_name,
	}
	return render(request, 'core/home.html', context)

