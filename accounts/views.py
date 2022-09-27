from django.shortcuts import render
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.urls import reverse_lazy

from .models import *
from .forms import *

# Create your views here.

# @receiver(user_logged_in)
class MyLoginView(LoginView):
# class MyLoginView(BSModalLoginView):
#class MyLoginView(BSModalUpdateView):
    template_name = 'registration/login.html'
    # template_name = 'registration/login_modal.html'
    authentication_form = MyLoginForm
    form_class = MyLoginForm
    success_message = 'Success: You were successfully logged in.'
    success_url = reverse_lazy('homepage:index')
    extra_context = dict(success_url=reverse_lazy('homepage:index'))
    # next = request.POST.get('next', '/')
    # return HttpResponseRedirect(next)

#   # def get_form_kwargs(self):
#   #   kwargs = super().get_form_kwargs()
#   #   kwargs['request'] = self.request
#   #   return kwargs


login_view_modal = MyLoginView.as_view()
