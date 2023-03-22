from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
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
def home_page(request):
    context = Context({
        'task_type': ALIGNMENT_TASK
    })
    context.update(csrf(request))
    return HttpResponse(get_template("Visualise/visualise.html").render(context))


@login_required
@ajax_required
def visualise_alignment(request, task_id):
    graphs = get_nodes_and_edges_for_task(task_id=task_id, user=request.user)
    context = Context({
        'graphs': graphs
    })
    return HttpResponse(get_template("Visualise/AlignmentVisualisation.html").render(context))


@login_required
@ajax_required
def visualise(request):
    LOGGER.info("User " + str(request.user.username) + ", Visualisation")
    networks = json.loads(request.POST["data"])["Networks"]
    nodes, edges = get_graph_nodes_and_edges(unicodedata.normalize('NFKD', networks[0][1]).encode('ascii', 'ignore'))
    context = Context({
        'nodes': nodes,
        'edges': edges
    })
    return HttpResponse(get_template("Visualise/SingleNetworkVisualisation.html").render(context))
