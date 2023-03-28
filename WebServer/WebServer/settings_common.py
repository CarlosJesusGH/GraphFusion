__author__ = 'varun'
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMINS = (
    ("Carlos Garcia-Hernandez", 'carlos.garcia2@bsc.es'),
    # ("Varun Verma", 'vv311@ic.ac.uk'),
)

MANAGERS = ADMINS


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ns#c2+t3u2m1dtq2r0$(9ckp6+y#2+p6_))=*3f12b0yv4*q5e'

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # custom apps
    'dashboard',
    'authentication',
    'NetworkAlignment',
    'PairwiseAnalysis',
    'utils',
    'UserProfile',
    'TaskFactory',
    'DataVsModelAnalysis',
    'AdminCenter',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'WebServer.urls'

WSGI_APPLICATION = 'WebServer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# Additional locations of static files
# STATICFILES_DIRS = os.path.dirname(os.path.abspath(__file__)) + '/../templates/static/'
STATICFILES_DIRS = [os.path.dirname(os.path.abspath(__file__)) + '/../templates/static/']
# STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static'), ]  # suggested in post https://stackoverflow.com/questions/34248423/getting-404-error-when-loading-bootstrap-based-homepage-in-django
# STATIC_ROOT = os.path.dirname(os.path.abspath(__file__)) + '/../templates/static/'
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# MEDIA URLS
MEDIA_ROOT = os.path.dirname(os.path.abspath(__file__)) + '/../templates/static/media'
MEDIA_URL = "static/media/"

TEMPLATE_DIRS = (os.path.dirname(os.path.abspath(__file__)) + '/../templates',)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    # 'django.core.context_processors.csrf',
)

AUTH_PROFILE_MODULE = "model.models.UserProfile"

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler"
)

LOGIN_URL = "/authentication/"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.dirname(os.path.abspath(__file__)) + "/../logs/log.log",
            'maxBytes': 200000,
            'backupCount': 200,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

# PYTHON_PATH = BASE_DIR + "/../../bin/python"
PYTHON_PATH = "/root/miniconda3/envs/GC3Env/bin/python"
