from .base import *

import json

from django.core.exceptions import ImproperlyConfigured

# Secure Secret Key Logic

# JSON-based secrets module
with open(os.path.join(BASE_DIR, 'secrets.json')) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    """Get the secret variable or return explicit exception."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = 'Set the {0} environment variable'.format(setting)
        raise ImproperlyConfigured(error_msg)


# Basic Settings

SECRET_KEY = get_secret('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*']

# Installed Apps

INSTALLED_APPS += [
    'core',
    'website',
]

# Databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data', 'db.sqlite3'),
    }
}

# Static Files

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media Uploads

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = 'jackdriscoll777@gmail.com'
EMAIL_HOST_PASSWORD = 'ckeevzvklypkvuhz'
EMAIL_USE_TLS = True

# SMS Backend

SENDSMS_BACKEND = 'website.backends.twilio.SmsBackend'
SENDSMS_TWILIO_ACCOUNT_SID = 'ACa37268f2b9a9abe55239044931339725'
SENDSMS_TWILIO_AUTH_TOKEN = get_secret('TWILIO_AUTH_TOKEN')

# Login Settings

LOGIN_URL = 'core:login'
DEFAULT_PAGE = 'website:home_page'

# Google ReCaptcha

RECAPTCHA_SECRET_KEY = get_secret('RECAPTCHA_SECRET_KEY')
RECAPTCHA_SITE_KEY = get_secret('RECAPTCHA_SITE_KEY')

# Proxy Settings


# 2019.09.02-DEA
