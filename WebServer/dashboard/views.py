__author__ = 'varun'

from django.template.loader import get_template
from django.http import HttpResponse
from django.template import Context
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from utils.UserUtils import get_name
from TaskFactory.views import get_task_view_objects_for_user
from authentication.home_page_queries import get_all_sample_networks


@login_required
def user_home_page(request):
    context = Context({'name': get_name(request),
                       'is_staff': request.user.is_staff,
                       'is_beta_tester': request.user.groups.filter(name='BetaTesters').exists(),
                       'networks': get_all_sample_networks(),
                       'title': 'Home'})
    context.update(csrf(request))
    return HttpResponse(get_template("dashboard/base_loggedin_home.html").render(context))


@login_required
def dashboard(request):
    result = get_task_view_objects_for_user(request=request)
    context = Context({'tasks': result})
    return HttpResponse(get_template("dashboard/results.html").render(context))