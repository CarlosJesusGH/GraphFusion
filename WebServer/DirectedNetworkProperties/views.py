from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from DataVsModelAnalysis.DataVsModelAnalysisResult import get_string_for_png
from django.core.context_processors import csrf
from .settings import DIRECTED_NETWORK_PROPERTIES_COMPUTATIONS_DIR, DIRECTED_NETWORK_PROPERTIES_TASK, DIRECTED_NETWORKS_NAMES_MAPPINGS_FILE_NAME, \
    DIRECTED_NETWORK_RESULT_VIEW_FILE_NAME, DEGREE_DISTRIBUTION_FILE
from .DirectedNetworkPropertiesAnalysis import make_system_call, get_network_properties_for_graphs
from django.contrib.auth.decorators import login_required
from utils.AJAX_Required import ajax_required
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import logging
import json
import unicodedata
import ast
import os

LOGGER = logging.getLogger(__name__)


@login_required
@ajax_required
def home_page(request):
    context = Context({
        'task_type': DIRECTED_NETWORK_PROPERTIES_TASK
    })
    context.update(csrf(request))
    return HttpResponse(get_template("DirectedNetworks/networkProperties/network_analysis.html").render(context))


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
    degree_distribution_file = DIRECTED_NETWORK_PROPERTIES_COMPUTATIONS_DIR + "/" + task.operational_directory + "/" + \
                               DEGREE_DISTRIBUTION_FILE
    fig.savefig(degree_distribution_file, format='png')
    return get_string_for_png(degree_distribution_file)


def get_view_for_task(task, user):
    file_path = DIRECTED_NETWORK_PROPERTIES_COMPUTATIONS_DIR + "/" + task.operational_directory + "/" + \
                DIRECTED_NETWORK_RESULT_VIEW_FILE_NAME
    if os.path.isfile(file_path):
        return HttpResponse(open(file_path).read())
    return HttpResponse("<h4>Error</h4>")


@login_required
@ajax_required
def analyse_networks(request):
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
    rendered_view = get_template("DirectedNetworks/networkProperties/properties.html").render(context)
    with open(DIRECTED_NETWORK_PROPERTIES_COMPUTATIONS_DIR + "/" + task.operational_directory +
                      "/" + DIRECTED_NETWORK_RESULT_VIEW_FILE_NAME, "w") as f:
        f.write(rendered_view)
    return HttpResponse(rendered_view)


def delete_data_for_task(task):
    operational_dir = DIRECTED_NETWORK_PROPERTIES_COMPUTATIONS_DIR + "/" + task.operational_directory
    if os.path.exists(operational_dir):
        result = make_system_call("rm -r " + operational_dir)
        return result.return_code == 0
    return True


def get_raw_data_for_task(task):
    result = []
    op_dir = DIRECTED_NETWORK_PROPERTIES_COMPUTATIONS_DIR + "/" + task.operational_directory
    mappings = ast.literal_eval(open(op_dir + "/" + DIRECTED_NETWORKS_NAMES_MAPPINGS_FILE_NAME).read())
    for file_name, network_name in mappings:
        result.append((network_name + ".ndump2", open(op_dir + "/" + file_name + ".res.ndump2").read()))
        result.append((network_name + ".png", open(op_dir + "/" + file_name + ".res_gcm73.png").read()))
    result.append(("degree_distribution.png", open(op_dir + "/" + DEGREE_DISTRIBUTION_FILE).read()))
    return result