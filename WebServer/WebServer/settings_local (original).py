__author__ = 'varun'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',

        # 'NAME': 'graphc3',
        # 'USER': 'vverma93',
        # 'PASSWORD': 'varun9193',
        # 'HOST': 'db4free.net',
        # 'PORT': '3306',

        'NAME': 'GraphFusion',
        'USER': 'root',
        'PASSWORD': 'root',
        'PORT': '3306',
        'HOST': '/Applications/MAMP/tmp/mysql/mysql.sock',
    }
}
