__author__ = 'varun'

from django.conf.urls import url
from .views import user_home_page, dashboard, upload_network, download_networks

urlpatterns = [
    url(r'^$', user_home_page),
    url(r'^gc/$', dashboard),
    url(r'^upload_network$', upload_network),
    url(r'^download_networks$', download_networks),
]