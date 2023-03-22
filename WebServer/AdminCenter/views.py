from django.contrib.auth.decorators import login_required
from utils.AJAX_Required import ajax_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from TaskFactory.TaskView import get_task_view_objects_for_tasks
from TaskFactory.queries import get_all_tasks
from .UserTasksView import get_all_user_views
from django.contrib.admin.views.decorators import staff_member_required
import logging

LOGGER = logging.getLogger(__name__)


@login_required
@ajax_required
@staff_member_required
def admin_page(request):
    context = Context({
        'tasks': get_task_view_objects_for_tasks(get_all_tasks()),
        'users': get_all_user_views()
    })
    return HttpResponse(get_template("AdminCenter/admin_page.html").render(context))