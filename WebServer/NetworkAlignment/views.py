import unicodedata
import json
import logging
import traceback
import os

from django.http import HttpResponse, HttpResponseBadRequest
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required

from utils.AJAX_Required import ajax_required
from .GRAALRunner import GRAALRunner, make_system_call
from .MIGRAALRunner import MIGRAALRunner
from .LGRAALRunner import LGRAALRunner
from .settings import ALIGNMENT_TASK, COMPUTATIONS_DIR, RESULTS_FILES
from .AlignmentResultsDataStructure import get_alignment_result_for_task as alignment_view_for_task
from django.db import connection
from utils.InputFormatter import check_input_format, check_column_list_format

LOGGER = logging.getLogger(__name__)


@login_required
@ajax_required
def network_alignment_page(request):
    context = Context({
        'task_type': ALIGNMENT_TASK
    })
    return HttpResponse(get_template("NetworkAlignment/network_alginment.html").render(context))


def _check_input(algorithm, options):
    print("algorithm", algorithm)
    # print("options", options)
    if algorithm == "graal":
        if len(options) != 2:
            return HttpResponseBadRequest("Invalid options for GRAAL")
        if float(options[0]) < 0 or float(options[0]) > 1:
            return HttpResponseBadRequest("Invalid alpha for GRAAL")
        if int(options[1]) < 0:
            return HttpResponseBadRequest("Invalid seed for GRAAL")
    elif algorithm == "mi-graal":
        if len(options) != 1:
            return HttpResponseBadRequest("Invalid options for MI-GRAAL")
        if options[0] != "1" and options[0] != "2" and options[0] != "4" and options[0] != "8" and options[0] != "32":
            return HttpResponseBadRequest("Invalid cost matrix for MI-GRAAL")
    elif algorithm == "l-graal":
        print("options[0][:100]", options[0][:100])
        if len(options) != 1:
            return HttpResponseBadRequest("Invalid options for L-GRAAL")
        check_response, options[0] = check_column_list_format(options[0], num_of_columns=3, col_id_numerical=[2], parsed_delimiter='\t', verbose=False)
        if not check_response:
            err_msg = "Invalid sequence similarity file for L-GRAAL. " + (options[0] if options[0] is not None else "")
            return HttpResponseBadRequest(err_msg)
    else:
        return HttpResponseBadRequest("Invalid algorithm")
    return False

@login_required
@ajax_required
def submit_network_alignment_task(request):
    LOGGER.info("Received alignment request")
    try:
        data = json.loads(request.POST["networks"])["Networks"]
        # Check the input file format
        for network in data:
            check_response, network[1] = check_input_format(network[1], input_task_or_type='undirected', preferred_format='edgelist', verbose=False)
            if not check_response:
                err_msg = "Error: Incorrect format in input file '" + network[0] + "'. " + (network[1] if network[1] is not None else "")
                return HttpResponseBadRequest(err_msg)
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^
        networks = []
        for networkData in data:
            name = unicodedata.normalize('NFKD', networkData[0]).encode('ascii', 'ignore')
            network_list = unicodedata.normalize('NFKD', networkData[1]).encode('ascii', 'ignore')
            networks.append((name, network_list))
        if len(networks) is not 2:
            return HttpResponseBadRequest("Wrong number of networks")
        network1_name = networks[0][0]
        network2_name = networks[1][0]
        network1 = networks[0][1]
        network2 = networks[1][1]
        algorithm = request.POST["algorithm"]
        # LOGGER.info(request.POST["options"])
        options = json.loads(unicodedata.normalize('NFKD', request.POST["options"]).encode('ascii', 'ignore'))
        # Check the input options
        check_input_res = _check_input(algorithm, options)
        if check_input_res:
            return check_input_res
        task_name = request.POST["name"]
        # LOGGER.info("Received alignment request for algorithm:" + algorithm + " and option:" + str(options))
        if algorithm == "graal":
            aligner = GRAALRunner(graph1=network1,
                                  graph2=network2,
                                  graph1_name=network1_name,
                                  graph2_name=network2_name,
                                  alpha=float(options[0]),
                                  seed=options[1],
                                  user=request.user,
                                  name=task_name)
        elif algorithm == "mi-graal":
            aligner = MIGRAALRunner(graph1=network1,
                                    graph2=network2,
                                    graph1_name=network1_name,
                                    graph2_name=network2_name,
                                    cost_matrix=int(options[0]),
                                    user=request.user,
                                    name=task_name)
        elif algorithm == "l-graal":
            aligner = LGRAALRunner(graph1=network1,
                                   graph2=network2,
                                   graph1_name=network1_name,
                                   graph2_name=network2_name,
                                   sequence_similarity=options[0],
                                   user=request.user,
                                   name=task_name)
        else:
            return HttpResponseBadRequest("Invalid Algorithm")
        aligner.run_input_checks()
        connection.close()
        aligner.submit()
        return HttpResponse()
    except Exception as e:
        LOGGER.error(e)
        LOGGER.error(traceback.format_exc())
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)


def delete_data_for_task(task):
    operational_dir = COMPUTATIONS_DIR + "/" + task.operational_directory
    if os.path.exists(operational_dir):
        result = make_system_call("rm -r " + operational_dir)
        return result.return_code == 0
    return True

def get_view_for_task(task, user):
    return HttpResponse(alignment_view_for_task(task=task))


def get_raw_data_for_task(task):
    result = []
    for r_file in RESULTS_FILES:
        file_path = COMPUTATIONS_DIR + "/" + task.operational_directory + "/" + r_file
        if os.path.isfile(file_path):
            result.append([r_file, open(file_path).read()])
    return result