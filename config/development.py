
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'postgres',
        'PASSWORD': '12345678',
        'NAME': 'homely',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'test_mail@gmail.com'
EMAIL_HOST_PASSWORD = 'test_password'
EMAIL_PORT = 465
EMAIL_FROM_ADDRESS = 'test_email@gmail.com'
EMAIL_USE_SSL = True

SERVER_EMAIL = EMAIL_FROM_ADDRESS

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rw#o(k6f!@d*5d$fis1&u_z9-!0xlmly!msqhr2)7rlq*8e8ky'

def custom_show_toolbar(r):
    return False


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
}

INTERNAL_IPS = ('127.0.0.1', )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

