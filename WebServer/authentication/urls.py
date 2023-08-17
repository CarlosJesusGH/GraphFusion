__author__ = 'varun'

from django.conf.urls import url

from .Views import *


urlpatterns = [
    url(r'^register/', register),
    url(r'^authenticate/', login),
    url(r'^guest_login/', guest_login),
    url(r'^check-username/', check_username_exists),
    url(r'^logout/', logout),
    url(r'^contact/', contact_us),
    url(r'^$', home_page),
]