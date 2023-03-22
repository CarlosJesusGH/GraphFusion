__author__ = 'varun'
from django.contrib.auth.models import User
from TaskFactory.queries import get_all_running_tasks_for_user


class UserTasksView:
    username = ""
    name = ""
    email = ""
    number_of_tasks = ""

    def __init__(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_number_of_tasks(self):
        return self.number_of_tasks


def get_all_user_views():
    users = []
    for u in User.objects.all():
        user_view = UserTasksView(username=u.username)
        user_view.email = u.email
        user_view.name = u.first_name + " " + u.last_name
        user_view.number_of_tasks = len(get_all_running_tasks_for_user(u))
        users.append(user_view)
    return users