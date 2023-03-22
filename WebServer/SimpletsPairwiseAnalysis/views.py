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
from .SimpletsPairwiseAnalysis import *
from .SimpletsPairwiseAnalysisResult import *
from .SimpletsDataVsModel import SimpletsDataVsModel
from .SimpletsDataVsModelResult import get_all_dvm_results_for_task

LOGGER = logging.getLogger(__name__)

@login_required
@ajax_required
def analysis_page(request):
    context = Context({
        'task_type': SIMPLETS_PAIRWISE_ANALYSIS_TASK,
        'distances': DISTANCES
    })
    return HttpResponse(get_template("Simplets/pairwiseAnalysis/analysis.html").render(context))

@login_required
@ajax_required
def analysis_dvm(request):
    print("MODELS.items()", MODELS.items())
    context = Context({
        'task_type': SIMPLETS_DVM_ANALYSIS_TASK,
        'models': MODELS.items(),
        'distances': DISTANCES
    })
    return HttpResponse(get_template("Simplets/dataVsModelAnalysis/analysis.html").render(context))

@login_required
@ajax_required
def run_pairwise_analysis(request):
    # print("request.POST", request.POST)
    # print("request.FILES", request.FILES)   
    networks = json.loads(request.POST["data"])["Networks"]
    name = request.POST["name"]
    distances = map(lambda s: unicodedata.normalize('NFKD', s).encode('ascii', 'ignore'),
                    json.loads(request.POST["distances"]))
    LOGGER.info("Executing PairwiseAnalysis for: " + str(request.user.username) + " with distances: " + str(distances))
    graphs_1 = []
    graphs_2 = []
    #
    for net1 in networks[0]:
        graph_name = unicodedata.normalize('NFKD', net1[0]).encode('ascii', 'ignore')
        graph = unicodedata.normalize('NFKD', net1[1]).encode('ascii', 'ignore')
        graphs_1.append((graph_name, graph))
    #
    for net1 in networks[1]:
        graph_name = unicodedata.normalize('NFKD', net1[0]).encode('ascii', 'ignore')
        graph = unicodedata.normalize('NFKD', net1[1]).encode('ascii', 'ignore')
        graphs_2.append((graph_name, graph))
    graphs = [graphs_1, graphs_2]
    analysis = SimpletsPairwiseAnalysis(graphs=graphs, task_name=name, user=request.user, distances=distances)
    connection.close()
    analysis.submit()
    return HttpResponse("Submitted")

@login_required
@ajax_required
def run_dvm_analysis(request):
    # print("request.POST", request.POST)
    # print("request.FILES", request.FILES)   
    networks = map(lambda a: map(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore'), a),
                   json.loads(request.POST["networks"]))
    task_name = request.POST["name"]
    distances = map(lambda s: unicodedata.normalize('NFKD', s).encode('ascii', 'ignore'),
                    json.loads(request.POST["distances"]))
    models = map(lambda a: [unicodedata.normalize('NFKD', a[0]).encode('ascii', 'ignore'),
                            ast.literal_eval(unicodedata.normalize('NFKD', a[1]).encode('ascii', 'ignore'))],
                 json.loads(request.POST["models"]))
    SimpletsDataVsModel(graph_content=networks[0], models=models, task_name=task_name, user=request.user,
                        distances=distances).submit()
    return HttpResponse("Submitted")

def delete_data_for_task(task):
    operational_dir = COMPUTATIONS_DIR + "/" + task.operational_directory
    if os.path.exists(operational_dir):
        result = make_system_call("rm -r " + operational_dir)
        return result.return_code == 0
    return True

# for network properties type of request
def get_view_for_task_simple(task, user):
    file_path = COMPUTATIONS_DIR + "/" + task.operational_directory + "/" + RESULT_VIEW_FILE
    if os.path.isfile(file_path):
        return HttpResponse(open(file_path).read())
    return HttpResponse("<h4>Error</h4>")

def get_view_for_task(task, user):
    results = get_all_pairwise_analysis_results(task=task)
    return HttpResponse(
        get_template("Simplets/pairwiseAnalysis/result.html").render(Context({'results': results})))

def get_view_for_task_dvm(task, user):
    results = get_all_dvm_results_for_task(task=task)
    results_values = get_all_pairwise_analysis_results(task=task)
    return HttpResponse(
        get_template("Simplets/dataVsModelAnalysis/result.html").render(Context({'results': results, 'results_values': results_values})))

# for other types of request
def get_view_for_task_other(task, user):
    table_values, output_files = get_all_results(task=task)
    context = Context({
        'rows': table_values,
        'output_files': output_files,
        'task': task,
    })
    return HttpResponse(get_template("Simplets/pairwiseAnalysis/result.html").render(context))

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

