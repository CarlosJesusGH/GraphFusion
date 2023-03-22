__author__ = 'varun'


def get_name(request):
    return request.user.first_name