__author__ = 'varun'

from settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gc3',
        'USER': 'root',
        'PASSWORD': 'root',
        'PORT': '3306',
        'HOST': 'localhost',
    }
}
