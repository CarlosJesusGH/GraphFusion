__author__ = 'varun'

from django.conf.urls import url
from .views import home_page, visualise, visualise_alignment

urlpatterns = [
    url(r'^$', home_page),
    url(r'^network/$', visualise),
    url(r'^alignment/(\d+)/$', visualise_alignment),
]