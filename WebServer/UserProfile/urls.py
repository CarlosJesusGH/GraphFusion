__author__ = 'varun'
from .views import settings_page, update_user_profile
from django.conf.urls import url

urlpatterns = [
    url(r'^$', settings_page),
    url(r'^update-profile$', update_user_profile),
]