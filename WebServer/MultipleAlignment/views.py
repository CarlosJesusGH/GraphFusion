__author__ = 'carlos garcia-hernandez'

from types import TracebackType
from django.http import HttpResponse, HttpRequest
from django.http.response import HttpResponseBadRequest
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from utils.AJAX_Required import ajax_required
import logging
import json
import os
import csv
import unicodedata
from .settings import *
from utils.SystemCall import make_system_call
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage, FileSystemStorage
# task's own imports
from .MultipleAlignmentAnalysis import *
from .MultipleAlignmentResult import *
# from TaskFactory.views import get_task_view_objects_for_user

LOGGER = logging.getLogger(__name__)

@login_required
@ajax_required
def analysis_page(request):
    context = Context({
        'task_type': MULTIPLE_ALIGNMENT_TASK,
    })
    return HttpResponse(get_template("MultipleAlignment/analysis.html").render(context))

# from django.views.decorators.http import require_POST
# @require_POST
@login_required
@ajax_required
# @csrf_exempt
def submit_analysis(request):
    print("start submit_analysis")
    try:
        # print("request.POST", request.POST)
        # print("request.FILES", request.FILES)        
        data = json.loads(request.POST["data"])
        task_name = data["task_name"]
        max_iter = data["max_iter"]
        delta_min = data["delta_min"]
        data_networks = data["Networks"]
        ks = data["ks"]
        networks = []
        for networkData in data_networks:
            name = unicodedata.normalize('NFKD', networkData[0]).encode('ascii', 'ignore')
            network_list = unicodedata.normalize('NFKD', networkData[1]).encode('ascii', 'ignore')
            networks.append((name, network_list))
        # run analysis
        LOGGER.info("Executing MultipleAlignmentAnalysis for: " + str(request.user.username) + " with task_name: " + str(task_name))
        request_FILES = request.FILES
        task = MultipleAlignmentAnalysis(networks, request_FILES, task_name=task_name, user=request.user, max_iter=max_iter, delta_min=delta_min, ks=ks)
        task.submit()
        data = json.dumps({
        'msg': "Successfully submitted task " + task_name,
        })
        return HttpResponse(data)
    except Exception as e:
        LOGGER.error(e)
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)

# not used yet
def MultipleAlignment_extra_task(request):
    # check example in similar task like computed psb_matcomp
    print("start compute_template_extra")
    try:
        print("request.POST", request.POST)
        print("request.FILES", request.FILES)
        data = json.dumps({
        'msg': "Successfully computed psb_matcomp",
        'psb_matcomp_pred': [("candidate_0", "confidence_0"), ("candidate_1", "confidence_1"), ("candidate_2", "confidence_2")],
        # 'psb_matcomp_pred': table_values,
        })
        return HttpResponse(data)
    except Exception as e:
        LOGGER.error(e)
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)


def delete_data_for_task(task):
    operational_dir = COMPUTATIONS_DIR + "/" + task.operational_directory
    if os.path.exists(operational_dir):
        result = make_system_call("rm -r " + operational_dir)
        return result.return_code == 0
    return True

def get_view_for_task_html(task, user):
    file_path = NETWORK_PROPERTIES_COMPUTATIONS_DIR + "/" + task.operational_directory + "/" + \
                NETWORK_RESULT_VIEW_FILE_NAME
    if os.path.isfile(file_path):
        return HttpResponse(open(file_path).read())
    return HttpResponse("<h4>Error</h4>")

def get_view_for_task(task, user):
    table_values, output_files = get_all_results(task=task)
    context = Context({
        'rows': table_values,
        'output_files': output_files,
        'task': task,
    })
    return HttpResponse(get_template("MultipleAlignment/result.html").render(context))

def get_raw_data_for_task(task):
    return get_all_downloadable_results(task)

# ---------------------------------
# tasks related functions

from TaskFactory.models import Task

def get_task_with_id(task_id):
    return Task.objects.get(taskId=task_id)

