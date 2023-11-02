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
from utils.InputFormatter import check_input_format, check_column_list_format

LOGGER = logging.getLogger(__name__)

@login_required
@ajax_required
def analysis_page(request):
    context = Context({
        'task_type': MULTIPLE_ALIGNMENT_TASK,
    })
    return HttpResponse(get_template("MultipleAlignment/analysis.html").render(context))


def _check_input(max_iter, delta_min, ks, request_FILES):
    if int(max_iter) <= 0:
        return HttpResponseBadRequest("Invalid max_iter")
    if float(delta_min) <= 0:
        return HttpResponseBadRequest("Invalid delta_min")
    if len(ks) == 0:
        return HttpResponseBadRequest("Invalid ks")
    else:
        # Split ks by spaces or commas depending on the input
        ks = ks.split(",") if "," in ks else ks.split()
        for k in ks:
            if int(k) <= 0:
                return HttpResponseBadRequest("Invalid ks")
    if len(request_FILES) == 0:
        return HttpResponseBadRequest("Invalid sequence similarity file")
    if REQUEST_FILES[0] not in request_FILES:
        return HttpResponseBadRequest("Invalid sequence similarity file")
    # Read TemporaryUploadedFile into string
    sequence_sim = request_FILES[REQUEST_FILES[0]].read().decode("utf-8")
    check_response, sequence_sim = check_column_list_format(sequence_sim, num_of_columns=3, col_id_numerical=[2], parsed_delimiter=' ', add_headers= ["Gene1", "Gene2", "Association_strength"], verbose=False)
    if not check_response:
        err_msg = "Invalid sequence similarity file. " + (sequence_sim if sequence_sim is not None else "")
        return HttpResponseBadRequest(err_msg)
    # print("sequence_sim[:100]", sequence_sim[:100])
    # Update TemporaryUploadedFile with new string
    request_FILES[REQUEST_FILES[0]] = ContentFile(sequence_sim.encode("utf-8"))
    return False

def _check_sequence_sim(data_networks, request_FILES):
    # Check that the sequence similarity file corresponds to the networks
    # print("data_networks", data_networks)
    # print("request_FILES", request_FILES)
    sequence_sim = request_FILES[REQUEST_FILES[0]].read().decode("utf-8")
    print("sequence_sim[:100]", sequence_sim[:100])
    # Get all the nodes from first two columns in the sequence similarity file. The third column is the association strength. The first row is the header.
    sequence_sim_nodes = set()
    for line in sequence_sim.split("\n")[1:]:
        if line.strip() == "":
            continue
        sequence_sim_nodes.add(line.split()[0])
        sequence_sim_nodes.add(line.split()[1])
    print("sequence_sim_nodes[:10]", list(sequence_sim_nodes)[:10])
    # Get all the nodes from the networks
    networks_nodes = set()
    for network in data_networks:
        for line in network[1].split("\n"):
            if line.strip() == "":
                continue
            networks_nodes.add(line.split()[0])
            networks_nodes.add(line.split()[1])
    print("networks_nodes[:10]", list(networks_nodes)[:10])
    # Check that all nodes in the sequence similarity file exists in the networks
    if not sequence_sim_nodes.issubset(networks_nodes):
        # Print the nodes that are not present in the networks
        print("sequence_sim_nodes - networks_nodes", sequence_sim_nodes - networks_nodes)
        return HttpResponseBadRequest("Invalid sequence similarity file, some nodes are not present in the networks")
    # Update TemporaryUploadedFile with new string
    # request_FILES[REQUEST_FILES[0]] = ContentFile(sequence_sim.encode("utf-8"))
    # Warning: every time you read a TemporaryUploadedFile, you need to reset the pointer to the beginning of the file
    request_FILES[REQUEST_FILES[0]].seek(0)
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
        data = json.loads(request.POST["data"])
        task_name = data["task_name"]
        max_iter = data["max_iter"]
        delta_min = data["delta_min"]
        ks = data["ks"]
        data_networks = data["Networks"]
        if False:
            # vvvvvvvvvvvvvvvvvvvvvvvvvvv
            # Check the input file format
            check_input_res = _check_input(max_iter, delta_min, ks, request.FILES)
            if check_input_res:
                return check_input_res
        if False:
            for network in data_networks:
                check_response, network[1] = check_input_format(network[1], input_task_or_type='undirected', preferred_format='edgelist', verbose=False)
                if not check_response:
                    err_msg = "Error: Incorrect format in input file '" + network[0] + "'. " + (network[1] if network[1] is not None else "")
                    return HttpResponseBadRequest(err_msg)
            # Check that the sequence similarity file corresponds to the networks
            check_input_res = _check_sequence_sim(data_networks, request.FILES)
            if check_input_res:
                return check_input_res
            # Warning: every time you read a TemporaryUploadedFile, you need to reset the pointer to the beginning of the file
            # sequence_sim = request.FILES[REQUEST_FILES[0]].read().decode("utf-8")
            # print("flag - sequence_sim", sequence_sim[:100])
            request.FILES[REQUEST_FILES[0]].seek(0)
            # ^^^^^^^^^^^^^^^^^^^^^^^^^^^
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
        return HttpResponseBadRequest(e.message)

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

