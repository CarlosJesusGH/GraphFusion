__author__ = 'carlos garcia-hernandez'  # using as reference: WebServer/CanonicalCorrelationAnalysis/urls.py

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', analysis_page),
    # url(r'^analysis_properties$', submit_analysis_properties),
    url(r'^analysis_backend$', submit_analysis_backend),
    # url(r'^extra_task$', extra_task),
]