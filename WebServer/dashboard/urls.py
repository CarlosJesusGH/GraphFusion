__author__ = 'varun'

from django.conf.urls import url
from .views import user_home_page, dashboard

urlpatterns = [
    url(r'^$', user_home_page),
    url(r'^gc/$', dashboard),
]