__author__ = 'varun'

from django.conf.urls import url
from .views import network_alignment_page, submit_network_alignment_task

urlpatterns = [
    url(r'^$', network_alignment_page),
    url(r'^submit-alignment/$', submit_network_alignment_task),
]