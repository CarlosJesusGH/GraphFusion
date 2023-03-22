__author__ = 'varun'

from django.conf.urls import url
from .views import analysis_page, submit_analysis

urlpatterns = [
    url(r'^$', analysis_page),
    url(r'^analyse$', submit_analysis),
]