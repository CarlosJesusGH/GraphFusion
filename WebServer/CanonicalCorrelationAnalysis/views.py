from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from utils.AJAX_Required import ajax_required
from .settings import CANONICAL_CORRELATION_TASK, os, CANONICAL_CORRELATION_COMPUTATIONS_DIR, ANNOTATIONS_TYPE
from utils.SystemCall import make_system_call
from .CanonicalAnalysis import CanonicalAnalysis
from .CanonicalAnalysisResult import get_all_results, get_all_downloadable_results
import logging
import json
import unicodedata

LOGGER = logging.getLogger(__name__)


@login_required
@ajax_required
def analysis_page(request):
    context = Context({
        'task_type': CANONICAL_CORRELATION_TASK,
        'annotations': ANNOTATIONS_TYPE
    })
    return HttpResponse(get_template("CanonicalCorrelationAnalysis/analysis.html").render(context))


@login_required
@ajax_required
def submit_analysis(request):
    data = json.loads(request.POST["data"])
    network = data["Networks"][0]
    task_name = request.POST["task_name"]
    name = unicodedata.normalize('NFKD', network[0]).encode('ascii', 'ignore')
    network_list = unicodedata.normalize('NFKD', network[1]).encode('ascii', 'ignore')
    annotation_type = None
    annotations = None
    if "annotation_type" in data:
        annotation_type = unicodedata.normalize('NFKD', data["annotation_type"]).encode('ascii', 'ignore')
    elif "annotations" in data:
        annotations = unicodedata.normalize('NFKD', data["annotations"]).encode('ascii', 'ignore')
    use_log_scale = request.POST["use_log_scale"]
    task = CanonicalAnalysis(name=task_name, user=request.user, graph=network_list, graph_name=name,
                             log_scale=use_log_scale, annotations_type=annotation_type, annotations=annotations)
    task.submit()
    return HttpResponse("Successfully submitted")


def get_view_for_task(task, user):
    results, overflow = get_all_results(task=task)
    context = Context({
        'results': results,
        'overflow': overflow
    })
    return HttpResponse(get_template("CanonicalCorrelationAnalysis/result.html").render(context))


def delete_data_for_task(task):
    operational_dir = CANONICAL_CORRELATION_COMPUTATIONS_DIR + "/" + task.operational_directory
    if os.path.exists(operational_dir):
        result = make_system_call("rm -r " + operational_dir)
        return result.return_code == 0
    return False


def get_raw_data_for_task(task):
    return get_all_downloadable_results(task)