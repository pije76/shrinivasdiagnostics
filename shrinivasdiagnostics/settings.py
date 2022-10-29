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
    'core',
    'shop',
    # 'cart',
    # 'orders',
    'payment',

    'cities_light',
    'phonenumber_field',
    'django_summernote',
	'crispy_forms',
	'crispy_bootstrap5',
    'widget_tweaks',
    'bootstrap_modal_forms',
	'selectable',
    'paypal.standard.ipn',
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

AUTH_USER_MODEL = 'accounts.Profile'

AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend',
]

SITE_ID = 1

####################################################################################################

LOGIN_REDIRECT_URL = 'core:homepage'

SUMMERNOTE_THEME = 'bs4'

PHONENUMBER_DB_FORMAT = 'E164'
PHONENUMBER_DEFAULT_REGION = 'IN'
PHONENUMBER_DEFAULT_FORMAT = 'E164'

CITIES_LIGHT_TRANSLATION_LANGUAGES = ['en']
CITIES_LIGHT_INCLUDE_COUNTRIES = ['IN']
CITIES_LIGHT_INCLUDE_CITY_TYPES = ['PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC', 'PPLF', 'PPLG', 'PPLL', 'PPLR', 'PPLS', 'STLMT',]

# SELECT2_JS = 'easy_select2/vendor/select2-4.0.13/js/select2.min.js'
# SELECT2_JS = 'easy_select2/js/easy_select2.js'
# SELECT2_CSS = 'css/select2.css'
# SELECT2_CSS = 'easy_select2/css/easy_select2.css'
# SELECT2_USE_BUNDLED_JQUERY = True
# SELECT2_USE_BUNDLED_SELECT2 = True
# SELECT2_BOOTSTRAP = True
# SELECT2_CACHE_BACKEND = "select2"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

BOOTSTRAP4 = {
	'include_jquery': True,
}

CART_SESSION_ID = 'cart'

# # Razorpay settings
############ test ##################### 
RAZORPAY_PUBLIC_KEY = 'rzp_test_tA7AbSk6m2cdv2'
RAZORPAY_SECRET_KEY = 'vPGDTwajuC4X6KDxln8ZvQRv'

# ########## live #####################
# RAZORPAY_PUBLIC_KEY = 'rzp_test_tA7AbSk6m2cdv2'
# RAZORPAY_SECRET_KEY = 'vPGDTwajuC4X6KDxln8ZvQRv'

# # Braintree settings
# BRAINTREE_MERCHANT_ID = 'BRAINTREE_MERCHANT_ID' # Merchant ID 
# BRAINTREE_PUBLIC_KEY = 'BRAINTREE_PUBLIC_KEY' # Public Key 
# BRAINTREE_PRIVATE_KEY = 'BRAINTREE_PRIVATE_KEY' # Private key 

# # Paypal settings
# PAYPAL_RECEIVER_EMAIL = 'PAYPAL_RECEIVER_EMAIL'
PAYPAL_TEST = True

HAYSTACK_CONNECTIONS = {
    'default': 
    {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'URL': 'http://127.0.0.1:9200/',
        # 'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
        'INDEX_NAME': 'shop_products',
    },
}

STRIPE_KEY = ""

MESSAGE_LEVEL = message_constants.DEBUG
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
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
