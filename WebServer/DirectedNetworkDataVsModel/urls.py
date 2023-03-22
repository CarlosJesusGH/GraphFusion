__author__ = 'varun'

from django.conf.urls import url
from .views import home_page, run_data_vs_model_analysis

urlpatterns = [
    url(r'^$', home_page),
    url(r'^analyse/$', run_data_vs_model_analysis),
]