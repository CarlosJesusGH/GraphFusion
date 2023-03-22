from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext
from django.template.loader import get_template
from django.core.context_processors import csrf
from .forms import UserProfileForm
from authentication.Authenticate import check_username_password_is_valid
from utils.JsonForms import parse_json_form_data
from utils.AJAX_Required import ajax_required
import logging

LOGGER = logging.getLogger(__name__)


@login_required
@ajax_required
def settings_page(request):
    profile_form = UserProfileForm(initial={'first_name': request.user.first_name,
                                            'last_name': request.user.last_name,
                                            'email': request.user.email})
    context = RequestContext(request, {
        'name': request.user.first_name,
        'profile': profile_form
    })
    context.update(csrf(request))
    return HttpResponse(get_template('UserProfile/Profile.html').render(context))


@login_required
@ajax_required
def update_user_profile(request):
    data = parse_json_form_data(request.POST["data"])
    LOGGER.info("Updating profile for user: " + request.user.username)
    if data:
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
        password = data["old_password"]
        new_password = data["new_password"]
        repeat_new_password = data["repeat_new_password"]
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        if check_username_password_is_valid(username=request.user.username,
                                            password=password) and new_password is repeat_new_password:
            request.user.set_password(new_password)
        request.user.save()
        return HttpResponse("success")
    else:
        LOGGER.error("Invalid form received for updating profile")
        return HttpResponseBadRequest("Invalid Form received.")