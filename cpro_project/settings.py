"""
Django settings for cpro_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('django_secret_key', '#yt2*mvya*ulaxd+6jtr#%ouyco*2%3ngb=u-_$44j^86g0$$3')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('django_debug', '1')))

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

if not DEBUG:
    ALLOWED_HOSTS = os.environ.get('django_allowed_hosts', '').split(',')

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'bootstrapform',
    'bootstrap_form_horizontal',
    'rest_framework',
    'storages',
    'web',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'web.middleware.httpredirect.HttpRedirectMiddleware',
)

ROOT_URLCONF = 'cpro_project.urls'

WSGI_APPLICATION = 'cpro_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if 'rds_hostname' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'cpro',
            'OPTIONS': {'charset': 'utf8mb4'},
            'USER': os.environ['rds_username'],
            'PASSWORD': os.environ['rds_password'],
            'HOST': os.environ['rds_hostname'],
            'PORT': os.environ['rds_port'],
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,
    'handlers': {
        'console': {
                        # logging handler that outputs log messages to terminal
            'class': 'logging.StreamHandler',
            'level': 'DEBUG', # message level to be written to console
                    },
            },
    'loggers': {
        '': {
                        # this sets root level logger to log debug and higher level
                                    # logs to console. All other loggers inherit settings from
                                                # root level logger.
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False, # this tells logger to send logging message
                                            # to its parent (will send if set to True)
                                                    },
        'django.db': {
                        # django also has database level logging
                                },
            },
    }

import sys
LOGGING = {
    'handlers': {
        'stderr': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stderr,
        }
    },
    'loggers': {
        'application': {
            'handlers': ['stderr'],
            'level': 'INFO',
        }
    }
}

STATIC_URL = '/static/'

SITE = 'cpro'

AUTHENTICATION_BACKENDS = ('web.backends.AuthenticationBackend',)

DEBUG_PORT = 8000

from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
  ('en', _('English')),
  ('es', _('Spanish')),
  ('ru', _('Russian')),
  ('fr', _('French')),
)

LANGUAGE_CODE = 'en'

LOCALE_PATHS = [
  os.path.join(BASE_DIR, 'web/locale'),
]

STATIC_UPLOADED_FILES_PREFIX = None

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'

TINYPNG_API_KEY = os.environ.get('tinypng_api_key', None)

TOTAL_DONATORS = 0
LATEST_NEWS = []
FAVORITE_CHARACTERS = []
STARTERS = []
MAX_STATS = {'visual_awakened_max': 7089, 'dance_awakened_max': 7089, 'vocal_awakened_max': 7089, 'overall_max': 12574, 'overall_awakened_max': 15291, 'hp_max': 40, 'visual_max': 5830, 'hp_awakened_max': 42, 'dance_max': 5830, 'vocal_max': 5830}

LOGIN_REDIRECT_URL = '/'
LOG_EMAIL = 'emails-log@schoolido.lu'
PASSWORD_EMAIL = 'password@schoolido.lu'
AWS_SES_RETURN_PATH = 'contact@schoolido.lu'

MAX_WIDTH = 1200
MAX_HEIGHT = 1200
MIN_WIDTH = 300
MIN_HEIGHT = 300

if 'aws_access_key_id' in os.environ:
    AWS_ACCESS_KEY_ID = os.environ.get('aws_access_key_id', 'your aws access key')
    AWS_SECRET_ACCESS_KEY = os.environ.get('aws_secret_access_key', 'your aws secret key')

    AWS_SES_REGION_NAME = os.environ.get('aws_ses_region_name', 'us-east-1')
    AWS_SES_REGION_ENDPOINT = os.environ.get('aws_ses_region_endpoint', 'email.us-east-1.amazonaws.com')

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_STORAGE_BUCKET_NAME = 'i.cinderella.pro'

    EMAIL_BACKEND = 'django_ses.SESBackend'
    from boto.s3.connection import OrdinaryCallingFormat
    AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()

from prod_generated_settings import *

try:
    from generated_settings import *
except ImportError, e:
    pass
try:
    from local_settings import *
except ImportError, e:
    pass

INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.append(SITE)

LOCALE_PATHS = list(LOCALE_PATHS)
LOCALE_PATHS.append(os.path.join(BASE_DIR, SITE, 'locale'))

if STATIC_UPLOADED_FILES_PREFIX is None:
    STATIC_UPLOADED_FILES_PREFIX = SITE + '/static/uploaded/' if DEBUG else 'u/'
