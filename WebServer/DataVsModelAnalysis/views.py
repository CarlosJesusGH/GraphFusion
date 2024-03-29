from django.contrib.auth.decorators import login_required
from utils.InputFormatter import check_input_format
from utils.AJAX_Required import ajax_required
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest
from django.template.loader import get_template
from django.template import Context
from .settings import DATA_VS_MODEL_TASK, MODELS, DATA_VS_MODEL_COMPUTATIONS_DIR, RESULT_IMAGE_FILES
from .DataVsModelAnalysis import DataVsModelAnalysis
from PairwiseAnalysis.PairwiseAnalysisResult import get_all_results
from .DataVsModelAnalysisResult import get_all_results_for_task
from PairwiseAnalysis.settings import DISTANCES
from utils.SystemCall import make_system_call
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
        'task_type': DATA_VS_MODEL_TASK,
        'models': MODELS.items(),
        'distances': DISTANCES
    })
    return HttpResponse(get_template('DataVsModelAnalysis/data_vs_model_analysis.html').render(context))


def get_view_for_task(task, user):
    results = get_all_results_for_task(task=task)
    results_values = get_all_pairwise_analysis_results(task=task)
    print("results_values", results_values)
    return HttpResponse(
        get_template("DataVsModelAnalysis/data_vs_model_result.html").render(Context({'results': results, 'results_values': results_values})))

def get_all_pairwise_analysis_results(task):
    result_values = get_all_results(task, directory=DATA_VS_MODEL_COMPUTATIONS_DIR)
    return result_values

def delete_data_for_task(task):
    operational_dir = DATA_VS_MODEL_COMPUTATIONS_DIR + "/" + task.operational_directory
    if os.path.exists(operational_dir):
        result = make_system_call("rm -r " + operational_dir)
        return result.return_code == 0
    return True


def get_raw_data_for_task(task):
    result = []
    for analysis_result in get_all_results(task, directory=DATA_VS_MODEL_COMPUTATIONS_DIR):
        result.append([analysis_result.f_name,
                       "\n".join([analysis_result.get_title()] + map("\t".join, [
                           analysis_result.get_heading()] + analysis_result.get_rows()))])
    for f_name, _ in RESULT_IMAGE_FILES.items():
        image_path = DATA_VS_MODEL_COMPUTATIONS_DIR + "/" + task.operational_directory + "/" + f_name
        if os.path.isfile(image_path):
            result.append([f_name, open(image_path).read()])
    return result


@login_required
@ajax_required
def run_data_vs_model_analysis(request):
    networks = map(lambda a: map(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore'), a), json.loads(request.POST["networks"]))
    # Check if the network format is correct
    for network in networks:
        response = check_input_format(network[1], input_task_or_type='undirected', preferred_format='edgelist')
        if not response[0]:
            return HttpResponseBadRequest("Error: Incorrect network format in network " + network[0] + ".")
        if response[1]:
            network[1] = response[1]
    task_name = request.POST["name"]
    distances = map(lambda s: unicodedata.normalize('NFKD', s).encode('ascii', 'ignore'),
                    json.loads(request.POST["distances"]))
    models = map(lambda a: [unicodedata.normalize('NFKD', a[0]).encode('ascii', 'ignore'),
                            ast.literal_eval(unicodedata.normalize('NFKD', a[1]).encode('ascii', 'ignore'))],
                 json.loads(request.POST["models"]))
    DataVsModelAnalysis(graph_content=networks[0], models=models, task_name=task_name, user=request.user,
                        distances=distances).submit()
    return HttpResponse("Submitted")