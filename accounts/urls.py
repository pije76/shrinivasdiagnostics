from django.contrib import admin
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.urls import path, re_path, include
from django.views.generic import RedirectView

# from accounts import views
from .views import *
from . import views

# from accounts.views import SignUpAutoComplete

app_name = 'accounts'

urlpatterns = [
    path('profile/<str:pk>/', profile_detail, name='profile_detail'),
    path('login-form/', login_view_modal, name='login_view_modal'),
    path('login/', user_login, name='user_login'),
    # path('signup/', user_signup, name='user_signup'),
    path('change-profile/', change_profile, name='change_profile'),

]

