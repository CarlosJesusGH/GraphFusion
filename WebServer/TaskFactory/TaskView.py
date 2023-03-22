__author__ = 'varun'

from .settings import TASK_ERROR_STATUS, TASK_FINISHED_STATUS, TASK_RUNNING_STATUS


def get_status_for_task(task):
    if not task.finished:
        return TASK_RUNNING_STATUS
    if task.error_occurred:
        return TASK_ERROR_STATUS
    return TASK_FINISHED_STATUS


def get_task_view_objects_for_tasks(tasks):
    result = []
    for t in tasks:
        task = TaskView(task_id=t.taskId)
        task.task_name = t.taskName
        task.start_time = t.started_at
        task.finish_time = t.finished_at
        task.finished = t.finished
        task.task_type = t.task_type
        task.status = get_status_for_task(t)
        task.user = t.user.username
        result.append(task)
    return result


class TaskView:
    task_name = ""
    start_time = None
    finish_time = None
    status = None
    finished = False
    task_type = ""
    user = None

    def __init__(self, task_id):
        self.task_id = task_id

    def get_task_type(self):
        return self.task_type

    def get_finished(self):
        return self.finished

    def get_task_id(self):
        return self.task_id

    def get_task_name(self):
        return self.task_name

    def get_start_time(self):
        return self.start_time

    def get_finish_time(self):
        return self.finish_time

    def get_status(self):
        return self.status

    def get_user(self):
        return self.user