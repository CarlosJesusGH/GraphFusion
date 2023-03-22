__author__ = 'varun'

from django.conf.urls import url
from .views import home_page, analyse_networks

urlpatterns = [
    url(r'^$', home_page),
    url(r'^analyse$', analyse_networks),
]