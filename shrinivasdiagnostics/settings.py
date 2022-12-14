"""
Django settings for shrinivasdiagnostics project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from django.contrib.messages import constants as message_constants
from django.contrib.messages import constants as messages

import os
import datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g3ury6i6%=d*yu1ss%1ho8-6$!=e1#18sk5z96@e0%hq3k&9(-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['shrinivasdiagnostics.com', '127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'accounts',
    'address',
    'homepage',
    'schedule',
    'shop',
    'order',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

	'crispy_forms',
	'crispy_bootstrap5',
    'widget_tweaks',
    'bootstrap_modal_forms',
    'frontend_forms',
    'django_select2',
    'massadmin',

    'cities_light',
    'phonenumber_field',
    # 'paypal.standard.ipn',
    'rest_framework',

    'whoosh_index',
    'haystack',
    'djoser',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shrinivasdiagnostics.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shrinivasdiagnostics.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # 'NAME': 'shrinivasdiagnostics',
        'USER': 'shrinivas',
        'PASSWORD': 'Shrinivas29*',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'assets/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "assets")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_USER_MODEL = 'accounts.Profile'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_FORMS = {'signup': 'accounts.forms.MySignUpForm'}
ACCOUNT_LOGOUT_REDIRECT_URL = "/"


LOGIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = 'homepage:index'
# LOGIN_REDIRECT_URL = 'accounts:user_login'
# LOGIN_REDIRECT_URL = '/accounts/login/'
# LOGOUT_REDIRECT_URL = 'accounts:user_login'
# LOGIN_URL = 'homepage:index'
# LOGOUT_URL = 'homepage:index'


SITE_ID = 1

MESSAGE_LEVEL = message_constants.DEBUG
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

FORM_RENDERER = 'django.forms.renderers.DjangoTemplates'

CITIES_LIGHT_APP_NAME = 'address'
####################################################################################################
SUMMERNOTE_THEME = 'bs4'

PHONENUMBER_DB_FORMAT = 'E164'
PHONENUMBER_DEFAULT_REGION = 'IN'
PHONENUMBER_DEFAULT_FORMAT = 'E164'

CITIES_LIGHT_TRANSLATION_LANGUAGES = ['en']
CITIES_LIGHT_INCLUDE_COUNTRIES = ['IN']
CITIES_LIGHT_INCLUDE_CITY_TYPES = ['PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC', 'PPLF', 'PPLG', 'PPLL', 'PPLR', 'PPLS', 'STLMT',]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

BOOTSTRAP4 = {
	'include_jquery': True,
}

# # Razorpay settings
############ test ##################### 

RAZORPAY_KEY_ID = 'rzp_test_3o6kPVKOmgfnM9'
RAZORPAY_KEY_SECRET = 'FsXFP5HO2Tb8uhjPcGYcMki8'

# ########## live #####################
# RAZORPAY_PUBLIC_KEY = 'rzp_test_tA7AbSk6m2cdv2'
# RAZORPAY_SECRET_KEY = 'vPGDTwajuC4X6KDxln8ZvQRv'

# # Paypal settings
# PAYPAL_RECEIVER_EMAIL = 'PAYPAL_RECEIVER_EMAIL'
PAYPAL_TEST = True


WHOOSH_INDEX = os.path.join(BASE_DIR, 'whoosh_index/')
# WHOOSH_INDEX = os.path.join(os.path.dirname(__file__), 'whoosh_index')

HAYSTACK_CONNECTIONS = {
    'default': 
    {
        # 'ENGINE': 'haystack.backends.elasticsearch5_backend.Elasticsearch5SearchEngine',
        # 'URL': 'http://127.0.0.1:9200/',
        # 'INDEX_NAME': 'haystack',
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': WHOOSH_INDEX,
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=15),
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
    },

}

####################################################################################################

# Override settings here
if DEBUG:
    INSTALLED_APPS += (
        'debug_toolbar',
	)
    INTERNAL_IPS = (
        '127.0.0.1',
    )
    DEBUG_TOOLBAR_CONFIG = {
		'INTERCEPT_REDIRECTS': False,
	}
    MIDDLEWARE += (
		'debug_toolbar.middleware.DebugToolbarMiddleware',
	)
    # TEMPLATES = [
	# 	{
	# 		'BACKEND': 'django.template.backends.django.DjangoTemplates',
	# 		'DIRS': [os.path.join(BASE_DIR, 'templates')],
	# 		'APP_DIRS': True,
	# 		'OPTIONS': 
    #         {
	# 			"debug": DEBUG,
	# 			'context_processors': 
    #             [
	# 				'django.template.context_processors.debug',
	# 				'django.template.context_processors.request',
	# 				'django.contrib.auth.context_processors.auth',
	# 				'django.template.context_processors.i18n',
	# 				'django.template.context_processors.media',
	# 				'django.template.context_processors.static',
	# 				'django.template.context_processors.tz',
	# 				'django.contrib.messages.context_processors.messages',

	# 			],
	# 			"string_if_invalid": '<< MISSING VARIABLE "%s" >>' if DEBUG else "",
	# 		},
	# 	},
	# ]
