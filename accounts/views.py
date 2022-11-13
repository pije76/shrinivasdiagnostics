from django.shortcuts import render
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .models import *
from .forms import *

from bootstrap_modal_forms.generic import BSModalLoginView

# Create your views here.
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
	page_title = _('Member Profile')
	# memberlist = Profile.objects.filter(member=request.user.id).values_list("id", flat=True).first()
	get_fullname = Profile.objects.filter(email=request.user).values_list("name", flat=True).first()
	# get_email = Profile.objects.filter(member=request.user).values_list("email", flat=True).first()
	get_birthdate = Profile.objects.filter(email=request.user).values_list("birth_date", flat=True).first()
	# get_birthcity = Profile.objects.filter(email=request.user).values_list("birth_city", flat=True).first()

	initial_dict = {
		'full_name': get_fullname,
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

		else:
			messages.warning(request, form.errors)
	else:
		form = ProfileForm(initial=initial_dict, instance=request.user)

	context = {
		'page_title': page_title,
		'form': form,
		'get_fullname': get_fullname,
		# 'get_lastname': get_lastname,
		# 'get_email': get_email,
		'get_birthdate': get_birthdate,
		# 'get_birthcity': get_birthcity,
	}

	return render(request, 'accounts/profile.html', context)

