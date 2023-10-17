__author__ = 'carlos garcia-hernandez'  # using as reference: WebServer/CanonicalCorrelationAnalysis/urls.py

from django.conf.urls import url
from .views import *

# from .views import HomeView

urlpatterns = [
    url(r'^clustering_and_enrichment_analysis/$', analysis_page),
    # url(r'^clustering_analysis/$', clustering_analysis),
    url(r'^compute_clusters/$', compute_clusters),
    # url(r'^enrichment_analysis/$', enrichment_analysis),
    url(r'^compute_enrichments/$', compute_enrichments),
    url(r'^visualize_factor/$', visualize_factor),
    url(r'^update_drugstone_container/', update_drugstone_container),
]