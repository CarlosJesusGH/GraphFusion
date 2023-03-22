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

LOGGER = logging.getLogger(__name__)


@login_required
@ajax_required
def network_alignment_page(request):
    context = Context({
        'task_type': ALIGNMENT_TASK
    })
    return HttpResponse(get_template("NetworkAlignment/network_alginment.html").render(context))


@login_required
@ajax_required
def submit_network_alignment_task(request):
    try:
        data = json.loads(request.POST["networks"])["Networks"]
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
        LOGGER.info(request.POST["options"])
        options = json.loads(unicodedata.normalize('NFKD', request.POST["options"]).encode('ascii', 'ignore'))
        task_name = request.POST["name"]
        LOGGER.info("Received alignment request for algorithm:" + algorithm + " and option:" + str(options))
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
        return HttpResponseBadRequest("Error occurred while processing GRAAL request: " + e.message)


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