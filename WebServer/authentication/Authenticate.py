__author__ = 'Varun'
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def register_user(username, password, firstname, lastname, email):
    user = User.objects.create_user(username=username, password=password, email=email, first_name=firstname,
                                    last_name=lastname)
    user.save()
    return True


def check_username_password_is_valid(username, password):
    return authenticate(username=username, password=password)


def does_username_exists(username):
    if User.objects.filter(username=username).count():
        return True
    return False


def authenticate_user(username, password, request):
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return user
    return None


def logout_user(request):
    logout(request)
