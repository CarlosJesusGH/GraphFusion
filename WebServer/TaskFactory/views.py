from django.contrib.auth.decorators import login_required
from utils.AJAX_Required import ajax_required
from .settings import VIEW_FUNCTION_MAPPINGS, TASK_TYPES, DELETE_TASK_FUNCTION_MAPPINGS, DOWNLOAD_RESULTS_FUNCTIONS
from django.http import HttpResponseBadRequest, HttpResponse, StreamingHttpResponse
from django.template.loader import get_template
from .queries import get_task_with_id, get_all_finished_tasks_for_user, get_all_tasks_for_user, \
    get_all_running_tasks_for_user, check_task_exists_with_task_id, get_all_successful_tasks_for_user
from .TaskView import get_task_view_objects_for_tasks
from django.template import Context
from zipfile import ZipFile
from TaskFactory.TaskFactorySingleton import terminate_task as terminate_task_for_user
import logging
from datetime import datetime
import json
from StringIO import StringIO
import os

LOGGER = logging.getLogger(__name__)


@login_required
@ajax_required
def get_task_view(request, task_id):
    task = get_task_with_id(task_id=task_id)
    if task:
        LOGGER.info("Rending view for Task: " + str(task) + " in dir: " + task.operational_directory)
        if task.error_occurred:
            return HttpResponse(
                get_template("dashboard/error_result.html").render(Context({
                    'error_text': task.error_text
                })))
        return VIEW_FUNCTION_MAPPINGS[task.task_type](task=task, user=request.user)
    LOGGER.error("Invalid Task ID received for viewing task view.")
    return HttpResponseBadRequest("Task ID is incorrect.")


def __get_tasks_for_user(user, task_type):
    tasks = []
    for t in get_all_finished_tasks_for_user(task_type=task_type, user=user):
        tasks.append((t.taskId, t.taskName))
    return tasks


def __get_successful_tasks_for_user(user, task_type):
    tasks = []
    for t in get_all_successful_tasks_for_user(task_type=task_type, user=user):
        tasks.append((t.taskId, t.taskName))
    return tasks


@login_required
@ajax_required
def get_task_view_objects_for_user(request):
    return get_task_view_objects_for_tasks(tasks=get_all_tasks_for_user(user=request.user))


@login_required
@ajax_required
def get_running_tasks_for_user(request):
    tasks = []
    for t in get_all_running_tasks_for_user(user=request.user):
        tasks.append(t.taskName)
    return HttpResponse(json.dumps(tasks))


@login_required
@ajax_required
def delete_task(request, task_id):
    task = get_task_with_id(task_id=task_id)
    if task and DELETE_TASK_FUNCTION_MAPPINGS[task.task_type](task=task):
        task.delete()
        return HttpResponse("Task successfully deleted.")
    return HttpResponseBadRequest("Error occurred while deleting task")

@login_required
@ajax_required
def delete_all_tasks(request):
    LOGGER.info("Deleting all tasks for user: " + str(request.user))
    tasks = get_all_tasks_for_user(user=request.user)
    for task in tasks:
        if task and DELETE_TASK_FUNCTION_MAPPINGS[task.task_type](task=task):
            task.delete()
        else:
            return HttpResponseBadRequest("Error occurred while deleting task")
    # Find all the directories containing the word 'computations' in the nameand delete them
    LOGGER.info("Deleting all remaining computations directories.")
    # Do this in python 'DIR=( $(find -name "computations" -type d) )'
    # Then do this in python 'for dir in DIR: os.rmdir(dir)'
    os.system("find -name 'computations' -type d -exec rm -rf {} +")
    for dir in os.listdir("."):
        if dir.startswith("computations"):
            # os.rmdir(dir)
            print("dir", dir)
    # Now do the same but recursively
    # os.system("find -name 'computations' -type d -exec rm -rf {} +")
    # for dir in os.listdir("."):
    #     if dir.startswith("computations"):
    #         os.rmdir(dir)

    
    # All tasks successfully deleted
    return HttpResponse("All tasks successfully deleted.")
    


@login_required
@ajax_required
def terminate_task(request, task_id):
    if check_task_exists_with_task_id(task_id=task_id):
        task = get_task_with_id(task_id=task_id)
        if (request.user.is_staff or task.user == request.user) \
                and terminate_task_for_user(task_id=task_id):
            task.finished = True
            task.finished_at = datetime.now()
            if request.user == task.user:
                task.error_text = "Task terminated by " + request.user.first_name + " " + request.user.last_name
            else:
                task.error_text = "Task terminated by Admin-" + request.user.first_name + " " \
                                  + request.user.last_name + "(" + request.user.email + ")"
            task.error_occurred = True
            task.save()
            return HttpResponse("Task successfully terminated")
        return HttpResponseBadRequest("Error occurred while terminating task")
    return HttpResponseBadRequest("Invalid Task ID")


@login_required
@ajax_required
def get_tasks_for_user(request, task_type):
    if task_type in TASK_TYPES:
        context = Context({
            'tasks': __get_tasks_for_user(task_type=task_type, user=request.user)
        })
        return HttpResponse(get_template("TaskFactory/tasks_for_user.html").render(context))
    return HttpResponseBadRequest("Type of task was invalid. Please send a valid request.")


@login_required
@ajax_required
def get_successful_tasks_for_user(request, task_type):
    if task_type in TASK_TYPES:
        context = Context({
            'tasks': __get_successful_tasks_for_user(task_type=task_type, user=request.user)
        })
        return HttpResponse(get_template("TaskFactory/tasks_for_user.html").render(context))
    return HttpResponseBadRequest("Type of task was invalid. Please send a valid request.")


@login_required
def get_task_results_for_download(request, task_id):
    LOGGER.info("Downloading results for task: " + str(task_id) + " by " + str(request.user))
    task = get_task_with_id(task_id=task_id)
    if task.error_occurred:
        pass
    if task.user != request.user:
        return HttpResponseBadRequest("Something went wrong. Please refresh the page.")
    if not DOWNLOAD_RESULTS_FUNCTIONS.has_key(task.task_type):
        return HttpResponseBadRequest("Something went wrong. Please refresh the page.")
    files = DOWNLOAD_RESULTS_FUNCTIONS[task.task_type](task)
    in_memory = StringIO()
    zip_f = ZipFile(in_memory, "a")
    for f_name, f_data in files:
        zip_f.writestr(f_name, f_data)

    # fix for Linux zip files read in Windows
    for file in zip_f.filelist:
        file.create_system = 0

    zip_f.close()
    in_memory.seek(0)
    response = StreamingHttpResponse(in_memory.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename={}'.format('task_results_' + str(task.taskName) + '.zip')
    return response