from django.http import HttpResponse

__author__ = 'varun'


class HttpResponseServerError(HttpResponse):
    status_code = 500