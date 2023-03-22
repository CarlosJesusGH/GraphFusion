__author__ = 'carlos garcia-hernandez'  # using as reference: WebServer/CanonicalCorrelationAnalysis/urls.py

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', analysis_page),
    url(r'^analyse/$', run_pairwise_analysis),
    url(r'^page_dvm/$', analysis_dvm),
    url(r'^analyse_dvm/$', run_dvm_analysis),
]