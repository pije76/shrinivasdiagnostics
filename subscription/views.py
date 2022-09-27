from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models.functions import Now
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from .models import *
from .forms import *

import datetime

# Create your views here.
class PackageView(ListView):
	model = Package
	template_name = 'subscription/index.html'

	def get_user_subscription(self):
		user_subscription_qs = Subscription.objects.filter(user=self.request.user)
		if user_subscription_qs.exists():
			return user_subscription_qs.first()
		return None

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		current_subscription = self.request
		context['current_subscription'] = str(current_subscription)
		return context


# index = PackageView.as_view()
def index(request):
	titles = _('Subscribe')

	context = {
		'titles': titles,
	}

	# get_trial = Subscription.objects.filter(member=request.user).values_list('subscription', flat=True).last()
	# getstatus_trial = Subscription.objects.filter(member=request.user, subscription=1).values_list('status', flat=True).last()
	# getstatus_standar = Subscription.objects.filter(member=request.user, subscription=2).values_list('status', flat=True).last()
	# getstatus_professional = Subscription.objects.filter(member=request.user, subscription=3).values_list('status', flat=True).last()
	# getstatus_enterprise = Subscription.objects.filter(member=request.user, subscription=4).values_list('status', flat=True).last()

	# if get_trial == 1 and getstatus_trial == "expired":
	# 	messages.warning(request, "You're Trial Package is expired. Please choose a package to continue")
		# return render(request, 'subscription.html', context)
		# return redirect('homepage:index')

	# if len(getstatus_trial) > 0:
	# if getstatus_trial is not None:
	# 	return render(request, 'subscription.html', context)
	# else:
	# if getstatus_trial is None and getstatus_standar is not None:
	# 	return render(request, 'subscription/subscription.html', context)

	# if getstatus_trial.exists():
	# if getstatus_trial is not None:
	# if len(getstatus_standar) > 0:
	# if Subscription.objects.filter(member=request.user, subscription=1).exists():
		# return redirect('subscription:subscription')
	# 	return render(request, 'subscription.html', context)
	# else:
	# 	return render(request, 'subscription/subscription.html', context)

	# if getstatus_trial is None or getstatus_standar is None or getstatus_professional or getstatus_enterprise is None:
		# return render(request, 'subscription/subscription.html', context)
	return render(request, 'subscription.html', context)


def subscription(request):
	titles = _('Subscribe')
	context = {
		'titles': titles,
	}

	return render(request, 'subscription.html', context)


# @login_required
@login_required(login_url="/accounts/signup/")
def trial(request):
	titles = _('Trial Package')
	plans = Package.objects
	member = MemberProfile.objects.filter(username=request.user).values_list('username', flat=True).first()
	get_status = Subscription.objects.filter(member=request.user).values_list('status', flat=True).first()
	get_active = Subscription.objects.filter(member=request.user).values_list('active', flat=True).first()

	start_date = datetime.datetime.now()
	expire_date = start_date + datetime.timedelta(days=14)

	initial_dict = {
		'member': request.user,
		'subscription': 1,
		# 'ticker': None,
		# 'indicator': None,
		'begin_date': start_date,
		'expired_date': expire_date,
		'active': True,
		# 'price': 1,
		# 'quantity': 1,
		'status': 'paid',
	}

	get_subscription = Subscription.objects.filter(member=request.user).values_list('subscription', flat=True).last()
	getstatus_trial = Subscription.objects.filter(member=request.user, subscription=1).values_list('status', flat=True).last()
	# getstatus_standar = Subscription.objects.filter(member=request.user, subscription=2).values_list('status', flat=True).last()
	# getstatus_professional = Subscription.objects.filter(member=request.user, subscription=3).values_list('status', flat=True).last()
	# getstatus_enterprise = Subscription.objects.filter(member=request.user, subscription=4).values_list('status', flat=True).last()

	# if get_trial == 1 and getstatus_trial == "expired":
	# 	messages.warning(request, "You're Trial Package is expired. Please choose a package to continue")
		# return render(request, 'subscription.html', context)
		# return redirect('homepage:index')


	# if get_status == "expired":
	if get_subscription == 1 and getstatus_trial == "expired":
		messages.warning(request, "You're already used Trial Package and your package is expired now. Please choose another package to continue")
		return redirect('subscription:index')

	if get_subscription == 1 and getstatus_trial == "paid":
		messages.warning(request, "You're already choose Trial Package.")
		return redirect('subscription:index')

		# if request.user.is_authenticated:
		# 	try:
		# 		if get_active == "active":
	# 				# return render(request, 'subscription/subscription.html', context)
					# return redirect('homepage:index')
				# else:
			# 		messages.success(request, "Your Trial package is active.")
			# except Subscription.DoesNotExist:
			# 	return redirect('subscription:index')

		return redirect('subscription:index')

	if request.method == "POST":
		form = PlanForm(request.POST or None)

		if form.is_valid():
			subscription = form.cleaned_data['subscription']

			if Subscription.objects.filter(subscription=subscription).exists():
				messages.error(request, 'You are already use Trial Package. Please choose another package to continue')
				return redirect('subscription:index')
			else:
				save_plan = Subscription()
				# save_plan.member = member
				save_plan.member = form.cleaned_data.get('member')
				save_plan.subscription = form.cleaned_data.get('subscription')
				# save_plan.ticker = form.cleaned_data.get('ticker')
				# save_plan.indicator = form.cleaned_data.get('indicator')
				save_plan.begin_date = form.cleaned_data.get('begin_date')
				save_plan.expired_date = form.cleaned_data.get('expired_date')
				save_plan.active = form.cleaned_data.get('active')
				# save_plan.price = form.cleaned_data.get('price')
				# save_plan.quantity = form.cleaned_data.get('quantity')
				save_plan.status = form.cleaned_data.get('status')
				save_plan.save()

				obj_instance = MemberProfile.objects.get(username=request.user)
				obj_instance.membership_type = "trial"
				obj_instance.save(update_fields=['membership_type'])

				# return redirect('homepage:index')
				messages.success(request, "Your Trial package is active.")
				return redirect('homepage:index')
		else:
			messages.warning(request, form.errors)
	else:
		form = PlanForm(initial=initial_dict)

	context = {
		'titles': titles,
		'form': form,
		'plans': plans,
	}

	return render(request, 'subscription/trial.html', context)


# @login_required
@login_required(login_url="/accounts/signup/")
def basic(request):
	titles = _('Basic Package')
	member = MemberProfile.objects.filter(username=request.user).values_list('username', flat=True).first()
	get_status = Subscription.objects.filter(member=request.user).values_list('status', flat=True).first()
	get_active = Subscription.objects.filter(member=request.user).values_list('active', flat=True).first()

	start_date = datetime.datetime.now()
	expire_date = start_date + datetime.timedelta(days=30)

	initial_dict = {
		'member': request.user,
		'subscription': 2,
		'begin_date': start_date,
		'expired_date': expire_date,
		'active': True,
		'price': 1,
		'quantity': 1,
		'status': 'waiting',
	}

	get_subscription = Subscription.objects.filter(member=request.user).values_list('subscription', flat=True).last()
	getstatus_standar = Subscription.objects.filter(member=request.user, subscription=1).values_list('status', flat=True).last()

	if get_subscription == 2 and getstatus_standar == "expired":
		messages.warning(request, "You're already used Basic Package and your package is expired now. Please choose another package to continue")
		return redirect('subscription:index')

	if get_subscription == 2 and getstatus_standar == "paid":
		messages.warning(request, "You're already choose Basic Package.")
		return redirect('subscription:index')

	# if get_status == "expired":
	# 	messages.warning(request, "You're Basic Package is expired. Please choose a package and renew it to continue")

# 	if request.user.is_authenticated:
# 		try:
# 			if get_active == "active":
# # 				# return render(request, 'subscription/subscription.html', context)
# 				return redirect('homepage:index')
# 			else:
# 				messages.warning(request, "You're already use Basic Package. Please choose a package to continue")
# 		except Subscription.DoesNotExist:
# 			return redirect('subscription:index')

# 	return redirect('subscription:index')

	if request.method == "POST":
		form = PlanForm(request.POST or None)

		if form.is_valid():
			save_plan = Subscription()
			# save_plan.member = member
			save_plan.member = form.cleaned_data.get('member')
			save_plan.subscription = form.cleaned_data.get('subscription')
			save_plan.ticker = form.cleaned_data.get('ticker')
			save_plan.indicator = form.cleaned_data.get('indicator')
			save_plan.begin_date = form.cleaned_data.get('begin_date')
			save_plan.expired_date = form.cleaned_data.get('expired_date')
			save_plan.active = form.cleaned_data.get('active')
			save_plan.price = form.cleaned_data.get('price')
			save_plan.quantity = form.cleaned_data.get('quantity')
			save_plan.status = form.cleaned_data.get('status')
			save_plan.save()

			obj_instance = MemberProfile.objects.get(username=request.user)
			obj_instance.membership_type = "basic"
			obj_instance.save(update_fields=['membership_type'])


			# return redirect('homepage:index')
			messages.info(request, "You are subscribe to Basic package. Please make payment to activate it.")
			return redirect('homepage:index')
		else:
			messages.warning(request, form.errors)
	else:
		form = PlanForm(initial=initial_dict)

	context = {
		'titles': titles,
		'form': form,
		# 'plans': plans,
	}

	return render(request, 'subscription/basic.html', context)


# @login_required
@login_required(login_url="/accounts/signup/")
def professional(request):
	titles = _('Professional Package')
	start_date = datetime.datetime.now()
	expire_date = start_date + datetime.timedelta(days=180)

	initial_dict = {
		'member': request.user,
		'subscription': 2,
		'begin_date': start_date,
		'expired_date': expire_date,
		'active': True,
		'price': 1,
		'quantity': 1,
		'status': 'waiting',
	}

	if request.method == "POST":
		form = PlanForm(request.POST or None)

		if form.is_valid():
			save_plan = Subscription()
			# save_plan.member = member
			save_plan.member = form.cleaned_data.get('member')
			save_plan.subscription = form.cleaned_data.get('subscription')
			save_plan.ticker = form.cleaned_data.get('ticker')
			save_plan.indicator = form.cleaned_data.get('indicator')
			save_plan.begin_date = form.cleaned_data.get('begin_date')
			save_plan.expired_date = form.cleaned_data.get('expired_date')
			save_plan.active = form.cleaned_data.get('active')
			save_plan.price = form.cleaned_data.get('price')
			save_plan.quantity = form.cleaned_data.get('quantity')
			save_plan.status = form.cleaned_data.get('status')
			save_plan.save()

			# return redirect('homepage:index')
			return redirect('homepage:index')
		else:
			messages.warning(request, form.errors)
	else:
		form = PlanForm(initial=initial_dict)

	context = {
		'titles': titles,
		'form': form,
		# 'plans': plans,
	}

	return render(request, 'subscription/professional.html', context)


# @login_required
@login_required(login_url="/accounts/signup/")
def enterprise(request):
	titles = _('Enterprise Package')
	start_date = datetime.datetime.now()
	expire_date = start_date + datetime.timedelta(days=360)

	initial_dict = {
		'member': request.user,
		'subscription': 2,
		'begin_date': start_date,
		'expired_date': expire_date,
		'active': True,
		'price': 1,
		'quantity': 1,
		'status': 'waiting',
	}

	if request.method == "POST":
		form = PlanForm(request.POST or None)

		if form.is_valid():
			save_plan = Subscription()
			# save_plan.member = member
			save_plan.member = form.cleaned_data.get('member')
			save_plan.subscription = form.cleaned_data.get('subscription')
			save_plan.ticker = form.cleaned_data.get('ticker')
			save_plan.indicator = form.cleaned_data.get('indicator')
			save_plan.begin_date = form.cleaned_data.get('begin_date')
			save_plan.expired_date = form.cleaned_data.get('expired_date')
			save_plan.active = form.cleaned_data.get('active')
			save_plan.price = form.cleaned_data.get('price')
			save_plan.quantity = form.cleaned_data.get('quantity')
			save_plan.status = form.cleaned_data.get('status')
			save_plan.save()

			# return redirect('homepage:index')
			return redirect('homepage:index')
		else:
			messages.warning(request, form.errors)
	else:
		form = PlanForm(initial=initial_dict)

	context = {
		'titles': titles,
		'form': form,
		# 'plans': plans,
	}

	return render(request, 'subscription/enterprise.html', context)


def plan(request, planname):
	titles = _('Subscription Plan')
	# plan = get_object_or_404(Subscription, pk=pk)
	plan = Subscription.objects.filter(subscription__title=planname)
	member = MemberProfile.objects.get(user_id=request.user)
	get_status = Subscription.objects.filter(user=member).values_list('status', flat=True).first()

	context = {
		'titles': titles,
		'plan': plan,
	}

	if get_status == "expired":
		if request.user.is_authenticated:
			try:
				if request.user.active == "active":
					# return render(request, 'subscription/subscription.html', context)
					return redirect('homepage:index')
			except Subscription.DoesNotExist:
				return redirect('subscription:subscribe')
		return redirect('subscription:subscribe')
		# return redirect('homepage:index')
	else:
		return render(request, 'subscription/plan_detail.html', context)


def checkout(request):
	plan = get_object_or_404(Subscription, pk=pk)

	try:
		if plan.user.status == "paid":
			return redirect('settings')
	except Subscription.DoesNotExist:
		pass

	coupons = {'christmas': 31, 'welcome': 10}

	if request.method == 'POST':
		stripe_customer = stripe.Subscription.create(email=request.user.email, source=request.POST['stripeToken'])
		plan = 'price_1IhW37C4G22E1tTDA5Z5v4ij'

		if request.POST['plan'] == 'yearly':
			plan = 'price_1IhW90C4G22E1tTDkM2DTALW'

		if request.POST['coupon'] in coupons:
			percentage = coupons[request.POST['coupon'].lower()]
			try:
				coupon = stripe.Coupon.create(duration='once', id=request.POST['coupon'].lower(), percent_off=percentage)
			except:
				pass
			subscription = stripe.Subscription.create(customer=stripe_customer.id, items=[{'plan': plan}], coupon=request.POST['coupon'].lower())
		else:
			subscription = stripe.Subscription.create(customer=stripe_customer.id, items=[{'plan': plan}])

		customer = Subscription()
		customer.user = request.user
		customer.stripeid = stripe_customer.id
		customer.subscription = True
		customer.cancel_at_period_end = False
		customer.stripe_subscription_id = subscription.id
		customer.save()

		return redirect('home')
	else:
		coupon = 'none'
		plan = 'monthly'
		price = 2000
		og_dollar = 20
		coupon_dollar = 0
		final_dollar = 20

		if request.method == 'GET' and 'plan' in request.GET:
			if request.GET['plan'] == 'yearly':
				plan = 'yearly'
				price = 20000
				og_dollar = 200
				final_dollar = 200
		if request.method == 'GET' and 'coupon' in request.GET:
			if request.GET['coupon'].lower() in coupons:
				coupon = request.GET['coupon'].lower()
				percentage = coupons[request.GET['coupon'].lower()]

				coupon_price = int((percentage / 100) * price)
				price = price - coupon_price
				coupon_dollar = str(coupon_price)[:-2] + '.' + str(coupon_price)[-2:]
				final_dollar = str(price)[:-2] + '.' + str(price)[-2:]

		context = {
			'titles': titles,
			'plan': plan,
			'coupon': coupon,
			'price': price,
			'og_dollar': og_dollar,
			'coupon_dollar': coupon_dollar,
			'final_dollar': final_dollar,
		}

		return render(request, 'subscription/checkout.html', context)


def settings(request):
	subscription = False
	cancel_at_period_end = False

	if request.method == 'POST':
		subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
		subscription.cancel_at_period_end = True
		request.user.customer.cancel_at_period_end = True
		cancel_at_period_end = True
		subscription.save()
		request.user.customer.save()
	else:
		try:
			if request.user.customer.subscription:
				subscription = True
			if request.user.customer.cancel_at_period_end:
				cancel_at_period_end = True
		except Subscription.DoesNotExist:
			subscription = False

	context = {
		'titles': titles,
		'subscription': subscription,
		'cancel_at_period_end': cancel_at_period_end,
	}

	return render(request, 'registration/settings.html', context)


@user_passes_test(lambda u: u.is_superuser)
def updateaccounts(request):
	customers = Subscription.objects.all()
	for customer in customers:
		subscription = stripe.Subscription.retrieve(customer.stripe_subscription_id)
		if subscription.status != 'active':
			customer.subscription = False
		else:
			customer.subscription = True
		customer.cancel_at_period_end = subscription.cancel_at_period_end
		customer.save()
	return HttpResponse('completed')


def video_detail(request, pk):
	video = get_object_or_404(Video, id=pk)
	roadmap = video.course.roadmap
	sub = request.user.subscription

	has_active_sub = sub.is_active()
	has_access = sub.plan in roadmap.plan.all()

	if has_active_sub and has_access:
		return render(request, "video_player.html")

	return render(request, "upgrade_subscription.html")


