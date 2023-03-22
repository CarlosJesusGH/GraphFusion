from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.db import connection
from utils.AJAX_Required import ajax_required
from .DirectedNetworkPairwise import DirectedNetworkPairwise, make_system_call
from .settings import DIRECTED_NETWORK_PAIRWISE_TASK, PAIRWISE_ANALYSIS_COMPUTATIONS_DIR, DISTANCES
from .DirectedNetworkPairwiseResult import get_all_pairwise_analysis_results
import json
import logging
import unicodedata
import os

LOGGER = logging.getLogger(__name__)


def get_view_for_task(task, user):
    results = get_all_pairwise_analysis_results(task=task)
    return HttpResponse(
        get_template("DirectedNetworks/PairwiseDataAnalysis/pairwise_analysis_result.html").render(Context({'results': results})))


@login_required
@ajax_required
def home_page(request):
    context = Context({
        'task_type': DIRECTED_NETWORK_PAIRWISE_TASK,
        'distances': DISTANCES
    })
    return HttpResponse(get_template("DirectedNetworks/PairwiseDataAnalysis/pairwise_data_analysis.html").render(context))


@login_required
@ajax_required
def run_pairwise_analysis(request):
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
    analysis = DirectedNetworkPairwise(graphs=graphs, task_name=name, user=request.user, distances=distances)
    connection.close()
    analysis.submit()
    return HttpResponse("Submitted")


def delete_data_for_task(task):
    operational_dir = PAIRWISE_ANALYSIS_COMPUTATIONS_DIR + "/" + task.operational_directory
    if os.path.exists(operational_dir):
        result = make_system_call("rm -r " + operational_dir)
        return result.return_code == 0
    return True


def get_raw_data_for_task(task):
    result = []
    for analysis_result in get_all_pairwise_analysis_results(task):
        result.append([analysis_result.f_name,
                       "\n".join([analysis_result.get_title()] + map("\t".join, [
                           analysis_result.get_heading()] + analysis_result.get_rows()))])
    return result