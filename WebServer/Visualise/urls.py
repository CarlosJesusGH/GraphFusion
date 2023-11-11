__author__ = 'varun'

from django.conf.urls import url
from .views import home_page, visualize, visualize_alignment, home_page_directed

urlpatterns = [
    url(r'^$', home_page),
    url(r'^directed/$', home_page_directed),
    url(r'^network/$', visualize),
    url(r'^alignment/(\d+)/$', visualize_alignment),
]