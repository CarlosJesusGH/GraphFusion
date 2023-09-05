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
import numpy as np
import matplotlib.pyplot as plt
import unicodedata
from .settings import *
from utils.SystemCall import make_system_call
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage, FileSystemStorage
# task's own imports
from .GraphletEigencentralitiesAnalysis import *
from .GraphletEigencentralitiesResult import *

LOGGER = logging.getLogger(__name__)

@login_required
@ajax_required
def analysis_page(request):
    context = Context({
        'task_type': GraphletEigencentralities_TASK,
    })
    return HttpResponse(get_template("GraphletEigencentralities/networkProperties/analysis.html").render(context))

@login_required
@ajax_required
def submit_analysis_properties(request):
    data = json.loads(request.POST["data"])["Networks"]
    task_name = request.POST["task_name"]
    networks = []
    for networkData in data:
        name = unicodedata.normalize('NFKD', networkData[0]).encode('ascii', 'ignore')
        network_list = unicodedata.normalize('NFKD', networkData[1]).encode('ascii', 'ignore')
        networks.append((name, network_list))
    heading, rows, deg_dists, gcm_raw_data, network_names, task = get_network_properties_for_graphs(
        graphs=networks,
        user=request.user,
        task_name=task_name)
    context = Context({
        'heading': heading,
        'rows': rows,
        'gcm_raw_data': gcm_raw_data,
        'network_names': network_names,
        'deg_dist': __save_deg_dist_image(deg_dists, task=task)
    })
    rendered_view = get_template("GraphletEigencentralities/networkProperties/result.html").render(context)
    with open(COMPUTATIONS_DIR + "/" + task.operational_directory +
                      "/" + RESULT_VIEW_FILE, "w") as f:
        f.write(rendered_view)
    return HttpResponse(rendered_view)

# from django.views.decorators.http import require_POST
# @require_POST
@login_required
@ajax_required
# @csrf_exempt
def analysis_other_like_MultAlign(request):
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
        LOGGER.info("Executing Analysis for: " + str(request.user.username) + " with task_name: " + str(task_name))
        request_FILES = request.FILES
        task = GraphletEigencentralitiesAnalysis(networks, request_FILES, task_name=task_name, user=request.user, max_iter=max_iter, delta_min=delta_min, ks=ks)
        task.submit()
        data = json.dumps({
        'msg': "Successfully submitted task " + task_name,
        })
        return HttpResponse(data)
    except Exception as e:
        LOGGER.error(e)
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)

# not used yet
def extra_task(request):
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

# for network properties type of request
def get_view_for_task(task, user):
    file_path = COMPUTATIONS_DIR + "/" + task.operational_directory + "/" + RESULT_VIEW_FILE
    if os.path.isfile(file_path):
        return HttpResponse(open(file_path).read())
    return HttpResponse("<h4>Error</h4>")

# for other types of request
def get_view_for_task_other(task, user):
    table_values, output_files = get_all_results(task=task)
    context = Context({
        'rows': table_values,
        'output_files': output_files,
        'task': task,
    })
    return HttpResponse(get_template("GraphletEigencentralities/networkProperties/result.html").render(context))

def get_raw_data_for_task(task):
    return get_all_downloadable_results(task)

def __combine_deg_dist(data):
    result = []
    data = np.array(data)
    for i in range(1, max(data) + 1):
        result.append(sum(data == i))
    return result

def __save_deg_dist_image(lists, task):
    fig = plt.figure()
    sub_plot = fig.add_subplot(111)
    x_upper_limit = -1
    y_upper_limit = -1
    for _, data in lists:
        dist = __combine_deg_dist(data)
        sub_plot.plot(dist)
        x_upper_limit = max(x_upper_limit, max(data))
        y_upper_limit = max(y_upper_limit, max(dist))
    sub_plot.legend(list(zip(*lists)[0]), loc="upper right")
    sub_plot.set_xlim([x_upper_limit * -0.1, x_upper_limit * 1.1])
    sub_plot.set_ylim([y_upper_limit * -0.1, y_upper_limit * 1.1])
    plt.ylabel('Number of Nodes')
    plt.xlabel('Degrees')
    sub_plot.set_title("Degree Distribution")
    degree_distribution_file = COMPUTATIONS_DIR + "/" + task.operational_directory + "/" + DEGREE_DISTRIBUTION_FILE
    fig.savefig(degree_distribution_file, format='png')
    return get_string_for_png(degree_distribution_file)

# ---------------------------------
# tasks related functions

from TaskFactory.models import Task

def get_task_with_id(task_id):
    return Task.objects.get(taskId=task_id)

