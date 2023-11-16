from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest
from django.template import Context
from django.template.loader import get_template
from utils.InputFormatter import check_input_format
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from utils.AJAX_Required import ajax_required
from .graph_properties import get_graph_nodes_and_edges, get_nodes_and_edges_for_task
from NetworkAlignment.settings import ALIGNMENT_TASK
import json
import unicodedata
import logging

LOGGER = logging.getLogger(__name__)


@login_required
@ajax_required
def home_page(request, directed=False):
    context = Context({
        'task_type': ALIGNMENT_TASK,
        'directed': directed
    })
    context.update(csrf(request))
    return HttpResponse(get_template("Visualise/visualise.html").render(context))

@login_required
@ajax_required
def home_page_directed(request):
    return home_page(request, directed=True)

@login_required
@ajax_required
def visualize_alignment(request, task_id):
    graphs = get_nodes_and_edges_for_task(task_id=task_id, user=request.user)
    context = Context({
        'graphs': graphs
    })
    return HttpResponse(get_template("Visualise/AlignmentVisualisation.html").render(context))


@login_required
@ajax_required
def visualize(request):
    LOGGER.info("User " + str(request.user.username) + ", Visualization")
    networks = json.loads(request.POST["data"])["Networks"]
    directed = request.POST["directed"]
    print("directed", directed)
    # print("networks", networks)
    for network in networks:
        response = check_input_format(network[1], input_task_or_type='visualization', preferred_format='edgelist')
        # print("response", response)
        if not response[0]: # type: ignore
            return HttpResponseBadRequest("Error: Incorrect network format in network " + network[0] + ".")
        if response[1]: # type: ignore
            network[1] = response[1] # type: ignore
            # print("Network " + network[0] + " converted to edgelist format.")
    nodes, edges = get_graph_nodes_and_edges(unicodedata.normalize('NFKD', networks[0][1]).encode('ascii', 'ignore'))
    # # Show warning if the network is too large
    # if len(nodes) > 500:
    #     LOGGER.warning("User " + str(request.user.username) + ", Visualization, Network too large")
    #     return HttpResponseBadRequest("Warning: Network too large to visualize.")
    # # Show warning if the network is too dense
    # density = len(edges) / (len(nodes) * (len(nodes) - 1))
    # if density > 0.1:
    #     print("density", density)
    #     LOGGER.warning("User " + str(request.user.username) + ", Visualization, Network too dense")
    #     return HttpResponseBadRequest("Warning: Network too dense to visualize.")
    context = Context({
        'nodes': nodes,
        'edges': edges,
        'directed': directed
    })
    return HttpResponse(get_template("Visualise/SingleNetworkVisualisation.html").render(context))
