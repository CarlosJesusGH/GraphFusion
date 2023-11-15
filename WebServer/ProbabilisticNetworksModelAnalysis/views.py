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
from .ProbabilisticNetworksModelAnalysis import *
from .ProbabilisticNetworksModelAnalysisResult import *
from utils.InputFormatter import check_input_format

LOGGER = logging.getLogger(__name__)

@login_required
@ajax_required
def analysis_page(request):
    context = Context({
        'task_type': PROBABILISTIC_NETWORKS_MODEL_ANALYSIS_TASK,
    })
    return HttpResponse(get_template("ProbabilisticNetworks/modelAnalysis/analysis.html").render(context))

def _check_input(request_POST, data):
    try:
        model_name = request_POST["model_name"]
        distribution_name = request_POST["distribution_name"]
        model_nodes = int(data["model_nodes"])
        model_radius = int(data["model_radius"])
        model_density = float(data["model_density"])
        distribution_mean = float(data["distribution_mean"])
        distribution_variance = float(data["distribution_variance"])
        # distribution_empirical_file = data["distribution_empirical_file"]
        if data["distribution_empirical_file"] == "" or data["distribution_empirical_file"] == "[]":
            distribution_empirical_file = ""
        else:
            distribution_empirical_file = json.loads(unicodedata.normalize('NFKD', data["distribution_empirical_file"]).encode('ascii', 'ignore'))[0]
        # print("model_name", model_name, "distribution_name", distribution_name, "model_nodes", model_nodes, "model_radius", model_radius, "model_density", model_density, "distribution_mean", distribution_mean, "distribution_variance", distribution_variance, "distribution_empirical_file", distribution_empirical_file)
    except Exception as e:
        LOGGER.error(e)
        print("request_POST, data", request_POST, data)
        return HttpResponseBadRequest("Error: Incorrect format in the values. Input could not be parsed.")
    if model_name == "hyper_geometric":
        # 1.1 Hyper Geometric:
        # G = Network_Models.get_Hyper_Geometric(Node=model_nodes, Radius=model_radius)
        if model_nodes < 10:
            return HttpResponseBadRequest("Error: Number of nodes must be a positive integer greater than 10.")
        if model_radius <= 0:
            return HttpResponseBadRequest("Error: Radius must be a positive integer.")
    elif model_name == "barabasi_albert" or model_name == "erdos_renyi":
        # 1.2 Barabasi
        # G = Network_Models.get_m_for_barabasi_albert(Nodes=model_nodes, density=model_density)
        # 1.3 Erdos Renyi
        # G = Network_Models.get_Erdos_Renyi(Nodes=model_nodes, density=model_density)
        if model_nodes < 10:
            return HttpResponseBadRequest("Error: Number of nodes must be a positive integer greater than 10.")
        if model_density <= 0 or model_density > 1:
            return HttpResponseBadRequest("Error: Density must be a positive float between 0 and 1.")
        
        model_edges = int(round(model_nodes/2 - np.sqrt(model_nodes**2/4 - model_nodes*(model_nodes-1)*model_density/2)))
        # m >= 1 and m < n
        if model_edges < 1 or model_edges >= model_nodes:
            return HttpResponseBadRequest("Error: Number of edges must be a positive integer less than the number of nodes. According to the number of nodes and the density, the number of edges is " + str(model_edges) + ".")
    else:
        return HttpResponseBadRequest("Error: Model name not recognized.")
    if distribution_name == "uniform":
        # 2.1.1 Uniform_distribution
        # distribution = Uniform_distribution(nodes=len(G.nodes))
        # distribution = Network_Models.Uniform_distribution(nodes=len(G.edges))
        pass
    elif distribution_name == "beta":
        # 2.1.2 Beta_distribution
        # Note: The mean is the average of a group of numbers, and the variance measures the average degree to which each number is different from the mean.
        # distribution = Network_Models.Beta_distribution(nodes=len(G.edges), mean=0.5, variance=0.2)
        # distribution = Network_Models.Beta_distribution(nodes=len(G.edges), mean=distribution_mean, variance=distribution_variance)
        if distribution_mean <= 0 or distribution_mean > 1:
            return HttpResponseBadRequest("Error: Mean must be a float between 0 and 1.")
        if distribution_variance <= 0 or distribution_variance > 1:
            return HttpResponseBadRequest("Error: Variance must be a float between 0 and 1.")
    elif distribution_name == "empirical":
        # 2.1.3 Empirical_Distribution
        # distribution = Network_Models.Empirical_Distribution(path=operational_dir+"distribution_empirical_file", size=len(G.edges))
        # distribution = Network_Models.Empirical_Distribution(path=operational_dir+distribution_empirical_file, size=len(G.edges))
        if distribution_empirical_file == "":
            return HttpResponseBadRequest("Error: Empirical distribution file is empty.")
        check_response, _ = check_input_format(distribution_empirical_file, input_task_or_type='probabilistic', preferred_format='edgelist', verbose=False)
        if not check_response:
            return HttpResponseBadRequest("Error: Incorrect format in the empirical distribution file.")
    return False

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
        task_name = request.POST["task_name"]
        data = json.loads(request.POST["data"])
        check_input_res = _check_input(request.POST, data)
        if check_input_res:
            return check_input_res
        # return HttpResponseBadRequest("Error: Incorrect format in network " + network[0] + ".")
        # Run analysis
        LOGGER.info("Executing Analysis for: " + str(request.user.username) + " with task_name: " + str(task_name))
        request_FILES = request.FILES
        task = ProbabilisticNetworksModelAnalysis(request.POST, data, request_FILES, task_name=task_name, user=request.user)
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
def get_view_for_task_properties(task, user):
    file_path = COMPUTATIONS_DIR + "/" + task.operational_directory + "/" + RESULT_VIEW_FILE
    if os.path.isfile(file_path):
        return HttpResponse(open(file_path).read())
    return HttpResponse("<h4>Error</h4>")

# for other types of request
def get_view_for_task(task, user):
    result_txt, output_files = get_all_results(task=task)
    context = Context({
        'result_txt': result_txt,
        'output_files': output_files,
        'task': task,
    })
    return HttpResponse(get_template("ProbabilisticNetworks/modelAnalysis/result.html").render(context))

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

