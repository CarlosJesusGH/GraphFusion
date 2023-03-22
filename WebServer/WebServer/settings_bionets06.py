__author__ = 'varun'

from settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ["bionets06.doc.ic.ac.uk", "graphcrunch.doc.ic.ac.uk"]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# session expire at browser close
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# wsgi scheme
os.environ['wsgi.url_scheme'] = 'https'

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
