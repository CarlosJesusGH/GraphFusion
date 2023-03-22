__author__ = 'varun'

import logging

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.core.context_processors import csrf
from Authenticate import register_user, authenticate_user, does_username_exists, logout_user
from Forms import LoginForm, RegisterForm
from .home_page_queries import get_all_features, get_all_descriptions
from .settings import REGISTER_ENABLED


LOGGER = logging.getLogger(__name__)


def register(request):
    form = RegisterForm(request.POST, prefix="reg")
    LOGGER.info("Registering User")
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        rep_password = form.cleaned_data["repeatPassword"]
        first_name = form.cleaned_data["firstName"]
        last_name = form.cleaned_data["lastName"]
        email = form.cleaned_data["email"]
        if does_username_exists(username):
            request.session["error"] = "Username already taken."
            return HttpResponseRedirect("/")
        elif password != rep_password:
            request.session["error"] = "Passwords while registering did not match."
            return HttpResponseRedirect("/")
        register_user(username, password, first_name, last_name, email)
        user = authenticate_user(username, password, request)
        LOGGER.info("Registered user: " + user.username)
        if user is not None:
            return HttpResponseRedirect("/")
    else:
        LOGGER.info(form.errors.as_data())
    return HttpResponseRedirect("/")


def login(request):
    form = LoginForm(request.POST, prefix="login")
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate_user(username, password, request)
        if user is not None:
            LOGGER.info("Logging in " + user.username)
            return HttpResponseRedirect("/dashboard/")
    request.session["error"] = 'Wrong username/password'
    return HttpResponseRedirect("/")


def check_username_exists(request):
    if request.is_ajax():
        username = request.POST["username"]
        if does_username_exists(username):
            return HttpResponse("yes")
        else:
            return HttpResponse("no")
    return HttpResponse("Invalid Query")


def logout(request):
    LOGGER.info("Logging Out: " + request.user.username)
    logout_user(request)
    return HttpResponseRedirect("/")


def contact_us(request):
    context = Context({'login_form': (LoginForm(prefix="login")),
                       'register_form': (RegisterForm(prefix="reg")),
                       'is_logged_in': request.user is not None and request.user.is_authenticated(),
                       'register_enabled': REGISTER_ENABLED})
    return HttpResponse(get_template("authentication/contact.html").render(context))


def home_page(request):
    context = Context({'login_form': (LoginForm(prefix="login")),
                       'register_form': (RegisterForm(prefix="reg")),
                       'descriptions': get_all_descriptions(),
                       'features': get_all_features(),
                       'is_logged_in': request.user is not None and request.user.is_authenticated(),
                       'register_enabled': REGISTER_ENABLED})

    try:
        error_text = request.session["error"]
        request.session["error"] = None
        context.update({"error_text": error_text})
    except KeyError:
        pass

    context.update(csrf(request))
    return HttpResponse(get_template("authentication/login_register_page.html").render(context))
