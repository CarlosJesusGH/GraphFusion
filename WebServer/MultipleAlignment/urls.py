__author__ = 'carlos garcia-hernandez'  # using as reference: WebServer/CanonicalCorrelationAnalysis/urls.py

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', analysis_page),
    url(r'^analyse$', submit_analysis),
    url(r'^MultipleAlignment_extra_task$', MultipleAlignment_extra_task),
]