from django.shortcuts import render
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from order.models import *

from bootstrap_modal_forms.generic import BSModalLoginView

# Create your views here.
def user_login(request):
	username = password = ''
	response_data = {}
	is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

	if request.POST and request.is_ajax:
		phone = request.POST['phone']
		password = request.POST['password']

		try:
			get_user_by_phone = UserAccount.objects.get(phone=phone)
			user_phone = get_user_by_phone.phone
			username = get_user_by_phone.user.get_username()
			get_user = User.objects.get(username=username)

			if get_user.check_password(password):
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
						response_data = {'login' : "Success"}
					else:
						url = "http://2factor.in/API/V1/"+API_KEY+"/SMS/" + user_phone + "/AUTOGEN/OTPSEND"
						payload = ""
						response = requests.request("GET", url, data=payload)
						otp_data = response.json()
						response_data['user'] = "not active"
						response_data['user_phone'] = user_phone
				else:
					response_data = {'user':"password wrong"}
		except UserAccount.DoesNotExist:
			# except ObjectDoesNotExist:
			response_data = {'user':"nouser"}
	else:
		username = password = ''
		response_data = {'login': "Failed"}
	return HttpResponse(JsonResponse(response_data))


# @receiver(user_logged_in)
# class MyLoginView(BSModalUpdateView):
# class MyLoginView(LoginView):
class MyLoginView(BSModalLoginView):
	template_name = 'accounts/login_modal.html'
	authentication_form = MyLoginForm
	form_class = MyLoginForm
	success_message = 'Success: You were successfully logged in.'
	success_url = reverse_lazy('core:homepage')
	extra_context = dict(success_url=reverse_lazy('core:homepage'))
    # next = request.POST.get('next', '/')
    # return HttpResponseRedirect(next)

#   # def get_form_kwargs(self):
#   #   kwargs = super().get_form_kwargs()
#   #   kwargs['request'] = self.request
#   #   return kwargs


login_view_modal = MyLoginView.as_view()


def profile_detail(request, pk):
	page_title = _('Account Profile')
	user_id = Profile.objects.get(email=request.user)
	full_name = user_id.full_name
	phone_number = user_id.phone_number
	email = user_id.email
	user_address = Address.objects.filter(user=user_id)
	user_order = Order.objects.filter(user=user_id, item_order=False).count()

	initial_dict = {
		# 'full_name': get_fullname,
		# 'birth_date': get_nataldate,
		# 'birth_city': get_birth_city,
		# 'longitude': get_city_longitude,
		# 'latitude': get_city_latitude,
		# 'member': memberlist,
	}

	if request.method == "POST":
		form = ProfileForm(request.POST or None)

		get_city_name = cache.get('get_city_name')
		get_city_longitude = cache.get('get_city_longitude')
		get_city_latitude = cache.get('get_city_latitude')

		if form.is_valid():

			profile = form.save(commit=False)
			# profile.full_name = form.cleaned_data['full_name']
			profile.full_name = form.cleaned_data.get('full_name')
			# profile.birth_city = form.cleaned_data['birth_city']
			profile.birth_city = form.cleaned_data.get('birth_city')
			# profile.birth_date = form.cleaned_data['birth_date']
			profile.birth_date = form.cleaned_data.get('birth_date')
			profile.save()
			messages.warning(request, form.errors)

		else:
			messages.warning(request, form.errors)
	else:
		form = ProfileForm(initial=initial_dict, instance=request.user)

	context = {
		'page_title': page_title,
		'form': form,
		'full_name': full_name,
		'phone_number': phone_number,
		'email': email,
		'user_address': user_address,
		'user_id': user_id,
		'user_order': user_order,
	}

	return render(request, 'accounts/profile.html', context)


@login_required
def change_profile(request):
    schema_name = connection.schema_name
    patients = UserProfile.objects.filter(username=request.user.username)
    logos = Client.objects.filter(schema_name=schema_name)
    titles = Client.objects.filter(schema_name=schema_name).values_list('title', flat=True).first()
    page_title = _('Change Profile')
    icnumbers = UserProfile.objects.filter(full_name=request.user)
    form = ChangeUserProfile(prefix='profile')
    themes = request.session.get('theme')

    if request.method == 'POST':
        form = ChangeUserProfile(request.POST or None, instance=request.user)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.full_name = form.cleaned_data['full_name']
            profile.email = form.cleaned_data['email']
            profile.ic_number = form.cleaned_data['ic_number']
            profile.save()

            messages.success(request, _('Your profile has been change successfully.'))
            return HttpResponseRedirect('/account/')
        else:
            messages.warning(request, form.errors)

    else:
        form = ChangeUserProfile(instance=request.user)

    context = {
        'patients': patients,
        'logos': logos,
        'titles': titles,
        'page_title': page_title,
        'navbar': 'account',
        'icnumbers': icnumbers,
        'form': form,
        "themes": themes,
    }

    return render(request, 'account/change.html', context)



def get_user_totp_device(self, user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device

    def get(self, request, format=None):
        user=request.user
        device = get_device(self, user)
        if not device:
            device = user.totpdevice_set.create(confirmed=False)
        url = device.config_url
        return Response(url, status=status.HTTP_201_CREATED)
