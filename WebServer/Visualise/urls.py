__author__ = 'varun'

from django.conf.urls import url
from .views import home_page, visualize, visualize_alignment

urlpatterns = [
    url(r'^$', home_page),
    url(r'^network/$', visualize),
    url(r'^alignment/(\d+)/$', visualize_alignment),
]