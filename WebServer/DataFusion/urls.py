__author__ = 'carlos garcia-hernandez'  # using as reference: WebServer/CanonicalCorrelationAnalysis/urls.py

from django.conf.urls import url
from .views import analysis_page, submit_analysis, compute_clusters, compute_enrichments, compute_icell, get_view_for_result_icell_analysis, compute_gdvs, compute_gdv_sims, get_task_view_psb, compute_psb_roc, compute_psb_pr, compute_psb_matcomp

urlpatterns = [
    url(r'^$', analysis_page),
    url(r'^analyse$', submit_analysis),
    url(r'^compute_clusters$', compute_clusters),
    url(r'^compute_enrichments$', compute_enrichments),
    url(r'^compute_icell$', compute_icell),
    url(r'^result_icell_analysis$', get_view_for_result_icell_analysis),
    url(r'^compute_gdvs$', compute_gdvs),
    url(r'^compute_gdv_sims$', compute_gdv_sims),
    url(r'^task_psb/(\d+)/$', get_task_view_psb),
    url(r'^compute_psb_roc$', compute_psb_roc),
    url(r'^compute_psb_pr$', compute_psb_pr),
    # url(r'^compute_psb_f1score$', compute_psb_f1score),
    url(r'^compute_psb_matcomp$', compute_psb_matcomp),
]