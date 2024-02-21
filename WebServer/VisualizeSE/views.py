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
from .VisualizeSEAnalysis import *
from .VisualizeSEResult import *
from utils.InputFormatter import check_input_format
import re

LOGGER = logging.getLogger(__name__)

@login_required
@ajax_required
def analysis_page(request, directed=False):
    context = Context({
        'task_type': VISUALIZESE_TASK,
        'directed': directed
    })
    return HttpResponse(get_template("VisualizeSE/analysis.html").render(context))

@login_required
@ajax_required
def home_page_directed(request):
    return analysis_page(request, directed=True)

@login_required
@ajax_required
def visualize_network(request):
    print("start visualize_network")
    try:
        task_name = request.POST["task_name"]        
        data = json.loads(request.POST["data"])
        data_networks = data["Networks"]
        directed = request.POST["directed"]
        networks = []
        for network in data_networks:
            check_response, network[1] = check_input_format(network[1], input_task_or_type='visualization', preferred_format='edgelist')
            if not check_response:
                err_msg = "Error: Incorrect format in input file '" + network[0] + "'. " + (network[1] if network[1] is not None else "")
            networks.append((network[0], network[1]))
        # run analysis
        LOGGER.info("Executing Analysis for: " + str(request.user.username) + " with task_name: " + str(task_name))
        request_FILES = request.FILES
        task = VisualizeSEAnalysis(networks, directed, request_FILES, task_name=task_name, user=request.user)
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

# for network properties type of request
def get_view_for_task(task, user):
    file_path = COMPUTATIONS_DIR + "/" + task.operational_directory + "/" + RESULT_VIEW_FILE
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            filedata = file.read()
            # Substitute everything between <head> and </head> with sub_str. This is because the vis packages are loaded in the 'header.html' file.
            sub_str = '<style type="text/css"> #mynetwork { width: 90%; height: 600px; } </style>'        
            filedata = re.sub(r'(?<=<head>)(.*?)(?=</head>)', sub_str, filedata, flags=re.DOTALL)
        return HttpResponse(filedata)
    return HttpResponse("<h4>Error</h4>")

# for other types of request
def get_view_for_task_other(task, user):
    table_values, output_files = get_all_results(task=task)
    context = Context({
        'rows': table_values,
        'output_files': output_files,
        'task': task,
    })
    return HttpResponse(get_template("VisualizeSE/result.html").render(context))

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
    fig.savefig(degree_distribution_file, format='svg')
    return get_string_for_svg(degree_distribution_file)

# ---------------------------------
# tasks related functions

from TaskFactory.models import Task

def get_task_with_id(task_id):
    return Task.objects.get(taskId=task_id)

