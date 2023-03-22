__author__ = 'varun'

from .models import Task


def get_all_finished_tasks_for_user(task_type, user):
    return Task.objects.filter(user=user, task_type=task_type, finished=True)


def get_all_successful_tasks_for_user(task_type, user):
    return Task.objects.filter(user=user, task_type=task_type, finished=True, error_occurred=False)


def get_all_tasks():
    return Task.objects.all()


def get_all_tasks_for_user(user):
    return Task.objects.filter(user=user)


def check_task_exists_with_task_id(task_id):
    return get_task_with_id(task_id) is not None


def get_all_running_tasks_for_user(user):
    return Task.objects.filter(user=user, finished=False)


def get_task_with_id(task_id):
    return Task.objects.get(taskId=task_id)