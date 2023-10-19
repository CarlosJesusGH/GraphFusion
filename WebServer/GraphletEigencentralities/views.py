__author__ = 'carlos garcia-hernandez'

from types import TracebackType
from django.http import HttpResponse, HttpRequest
from django.http.response import HttpResponseBadRequest
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from utils.InputFormatter import check_input_format
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
    return HttpResponse(get_template("GraphletEigencentralities/analysis.html").render(context))


@login_required
@ajax_required
def submit_analysis_backend(request):
    # print("start submit_analysis_backend")
    try:
        # print("request.POST", request.POST)
        # print("request.FILES", request.FILES)
        task_name = request.POST["task_name"]        
        data = json.loads(request.POST["data"])
        data_networks = data["Networks"]
        # Check if the network format is correct
        for network in data_networks:
            check_response, network[1] = check_input_format(network[1], input_task_or_type='undirected', preferred_format='edgelist')
            if not check_response:
                return HttpResponseBadRequest("Error: Incorrect format in network " + network[0] + ".")
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        networks = []
        for networkData in data_networks:
            name = unicodedata.normalize('NFKD', networkData[0]).encode('ascii', 'ignore')
            network_list = unicodedata.normalize('NFKD', networkData[1]).encode('ascii', 'ignore')
            networks.append((name, network_list))
        # run analysis
        LOGGER.info("Executing Analysis for: " + str(request.user.username) + " with task_name: " + str(task_name))
        request_FILES = request.FILES
        task = GraphletEigencentralitiesAnalysis(networks, request_FILES, task_name=task_name, user=request.user)
        task.submit()
        data = json.dumps({
        'msg': "Successfully submitted task " + task_name,
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

# for other types of request
def get_view_for_task(task, user):
    result_txt, output_files = get_all_results(task=task)
    context = Context({
        # 'heading': table_values[0],
        # 'rows': table_values[1:],
        'result_txt': result_txt,
        'output_files': output_files,
        'task': task,
    })
    return HttpResponse(get_template("GraphletEigencentralities/result.html").render(context))

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

