__author__ = 'varun'

from .views import get_task_view, get_tasks_for_user, delete_task, get_running_tasks_for_user, terminate_task, \
    get_successful_tasks_for_user, get_task_results_for_download
from django.conf.urls import url

urlpatterns = [
    url(r'^task/(\d+)/$', get_task_view),
    url(r'^running-tasks/$', get_running_tasks_for_user),
    url(r'^delete/(\d+)/$', delete_task),
    url(r'^terminate-task/(\d+)/$', terminate_task),
    url(r'^Success/(\w+)/$', get_successful_tasks_for_user),
    url(r'^DownloadResult/(\d+)/$', get_task_results_for_download),
    url(r'^(\w+)/$', get_tasks_for_user),
]