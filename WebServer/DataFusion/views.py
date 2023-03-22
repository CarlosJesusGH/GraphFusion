__author__ = 'carlos garcia-hernandez'  # using as reference: WebServer/CanonicalCorrelationAnalysis/views.py and WebServer/NetworkAlignment/views.py

# from django.shortcuts import render

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
from .DataFusionAnalysis import DataFusionAnalysis
from .settings import * #DATA_FUSION_TASK, COMPUTATIONS_DIR, FACTORIZATION_TYPE, FACTOR_INIT_TYPE, FACTOR_SHARE_DIRECTION, ICELL_FILENAME, ICELL_GDV_FILENAME, GDV_SIMS_COMP_FOLDER, GDV_SIMS_FILENAME, GDV_GENELIST_FILENAME, ICELL_GENELIST_FILENAME, ENRICHMENTS_ANNO_FILENAME
from utils.SystemCall import make_system_call
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage, FileSystemStorage
from .DataFusionAnalysisResult import get_df_result_for_task as df_view_for_task
# from .DataFusionAnalysisResult import get_all_results, get_all_downloadable_results
# from .DataFusionAnalysisResult import compute_clusters_for_factor, compute_enrichments_for_clusters, compute_icell_for_factor, compute_gdv_for_icell, compute_gdv_similarities, compute_psb_roc_for_factor
from .DataFusionAnalysisResult import *

# from TaskFactory.views import get_task_view_objects_for_user

LOGGER = logging.getLogger(__name__)

@login_required
@ajax_required
def analysis_page(request):
    context = Context({
        'task_type': DATA_FUSION_TASK,
        'factorizations': FACTORIZATION_TYPE,
        'initializations': FACTOR_INIT_TYPE,
        'factor_sharings': FACTOR_SHARE_DIRECTION,
    })
    return HttpResponse(get_template("DataFusion/analysis.html").render(context))

# from django.views.decorators.http import require_POST
# @require_POST
@login_required
@ajax_required
# @csrf_exempt
def submit_analysis(request):
    print("start submit_analysis")
    try:
        print("request.POST", request.POST)
        print("request.FILES", request.FILES)        
        data = json.loads(request.POST["data"])
        facts = data["facts"]
        task_name = data["task_name"]
        setup = data["setup"]
        net_names = data["net_names"]
        max_iter = data["max_iter"]
        delta_min = data["delta_min"]
        LOGGER.info("Executing DataFusionAnalysis for: " + str(request.user.username) + " with task_name: " + str(task_name))
        request_FILES = request.FILES
        task = DataFusionAnalysis(facts, net_names, request_FILES, task_name=task_name, setup=setup, user=request.user, max_iter=max_iter, delta_min=delta_min)
        task.submit()
        return HttpResponse("Successfully submitted task " + task_name)
    except Exception as e:
        LOGGER.error(e)
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)

def compute_psb_matcomp(request):
    print("start compute_psb_matcomp")
    try:
        print("request.POST", request.POST)
        print("request.FILES", request.FILES)
        data = json.loads(request.POST["data"])
        psb_matcomp_fact = data["psb_fact"]
        task_dir = data["task_dir"]
        operational_dir = COMPUTATIONS_DIR + "/" + task_dir
        LOGGER.info("Executing psb_matcomp for fact: " + str(psb_matcomp_fact) + " in dir: " + str(task_dir))
        save_file_to_dir(operational_dir, PSB_MATCOMP_ENTITYLIST_ROWS, request.FILES["psb_matcomp_entitylist_rows"])
        save_file_to_dir(operational_dir, PSB_MATCOMP_ENTITYLIST_COLS, request.FILES["psb_matcomp_entitylist_cols"])
        psb_matcomp_img = compute_psb_matcomp_for_factor(op_dir=operational_dir, fact_name=psb_matcomp_fact)

        with open(operational_dir + "/" + PSB_MATCOMP_OUT_FILES[1], 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            table_values = []
            for i,row in enumerate(reader):
                if i > 0:
                    # print("row", row)
                    table_values.append((row[0], row[1], row[2]))
        # print("table_values", table_values[0:10])
        table_values = sorted(table_values, key=lambda tup: tup[2], reverse=True)
        # print("sorted(table_values)", table_values[0:10])
        if len(table_values) > 100:
            table_values = table_values[0:100]
        # print("table_values", table_values)
        data = json.dumps({
        'msg': "Successfully computed psb_matcomp",
        'psb_matcomp_img': psb_matcomp_img[0],
        # 'psb_matcomp_pred': [("candidate_0", "confidence_0"), ("candidate_1", "confidence_1"), ("candidate_2", "confidence_2")],
        'psb_matcomp_pred': table_values,
        })
        return HttpResponse(data)
    except Exception as e:
        LOGGER.error(e)
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)

def compute_psb_pr(request):
    print("start compute_psb_pr")
    try:
        print("request.POST", request.POST)
        print("request.FILES", request.FILES)
        data = json.loads(request.POST["data"])
        psb_pr_fact = data["psb_fact"]
        task_dir = data["task_dir"]
        operational_dir = COMPUTATIONS_DIR + "/" + task_dir
        LOGGER.info("Executing psb_pr for fact: " + str(psb_pr_fact) + " in dir: " + str(task_dir))
        psb_pr_img = compute_psb_pr_for_factor(op_dir=operational_dir, fact_name=psb_pr_fact)
        data = json.dumps({
        'msg': "Successfully computed psb_pr",
        'psb_pr_img': psb_pr_img[0],
        })
        return HttpResponse(data)
    except Exception as e:
        LOGGER.error(e)
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)

def compute_psb_roc(request):
    print("start compute_psb_roc")
    try:
        print("request.POST", request.POST)
        print("request.FILES", request.FILES)
        data = json.loads(request.POST["data"])
        psb_roc_fact = data["psb_fact"]
        task_dir = data["task_dir"]
        operational_dir = COMPUTATIONS_DIR + "/" + task_dir
        LOGGER.info("Executing psb_roc for fact: " + str(psb_roc_fact) + " in dir: " + str(task_dir))
        psb_roc_img = compute_psb_roc_for_factor(op_dir=operational_dir, fact_name=psb_roc_fact)
        data = json.dumps({
        'msg': "Successfully computed psb_roc",
        'psb_roc_img': psb_roc_img[0],
        # 'psb_pr_img': psb_roc_img[1],
        # 'psb_f1score_img': psb_roc_img[2],
        # 'psb_matcomp_img': psb_roc_img[3],
        # 'psb_matcomp_pred': [("candidate_0", "confidence_0"), ("candidate_1", "confidence_1"), ("candidate_2", "confidence_2")],
        })
        return HttpResponse(data)
    except Exception as e:
        LOGGER.error(e)
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)

def compute_clusters(request):
    print("start compute_clusters")
    try:
        print("request.POST", request.POST)
        print("request.FILES", request.FILES)
        data = json.loads(request.POST["data"])
        cluster_fact = data["cluster_fact"]
        task_dir = data["task_dir"]
        operational_dir = COMPUTATIONS_DIR + "/" + task_dir
        LOGGER.info("Executing clustering for fact: " + str(cluster_fact) + " in dir: " + str(task_dir))
        save_file_to_dir(operational_dir, CLUSTERS_ENTITYLIST_FILENAME, request.FILES["clusters_entitylist_file"])
        clusters_img = compute_clusters_for_factor(op_dir=operational_dir, fact_name=cluster_fact)
        data = json.dumps({
        'msg': "Successfully computed clusters",
        'clusters_img': clusters_img[0],
        })
        return HttpResponse(data)
    except Exception as e:
        LOGGER.error(e)
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)

def compute_enrichments(request):
    print("start compute_enrichments")
    try:
        print("request.POST", request.POST)
        print("request.FILES", request.FILES)
        data = json.loads(request.POST["data"])
        cluster_fact = data["cluster_fact"]
        # enrichments_anno = data["enrichments_anno"]
        task_dir = data["task_dir"]
        operational_dir = COMPUTATIONS_DIR + "/" + task_dir
        LOGGER.info("Executing enrichments for fact: " + str(cluster_fact) + " and annotations in dir: " + str(task_dir))
        save_file_to_dir(operational_dir, ENRICHMENTS_ANNO_FILENAME, request.FILES["annotations"])
        enrichments_img = compute_enrichments_for_clusters(op_dir=operational_dir, fact_name=cluster_fact, enrichments_anno=ENRICHMENTS_ANNO_FILENAME)
        data = json.dumps({
        'msg': "Successfully computed enrichments",
        'enrichments_img': enrichments_img[0],
        })
        return HttpResponse(data)
    except Exception as e:
        LOGGER.error(e)
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)

def compute_icell(request):
    print("start compute_icell")
    try:
        print("request.POST", request.POST)
        print("request.FILES", request.FILES)
        data = json.loads(request.POST["data"])
        icell_fact = data["icell_fact"]
        task_dir = data["task_dir"]
        operational_dir = COMPUTATIONS_DIR + "/" + task_dir
        LOGGER.info("Computing iCell for fact: " + str(icell_fact) + " in dir: " + str(task_dir))
        # print("result_make_system_call", make_system_call("rm " + operational_dir + "/" + ICELL_FILENAME))
        save_file_to_dir(operational_dir, ICELL_GENELIST_FILENAME, request.FILES["genelist"])
        icell_res = compute_icell_for_factor(op_dir=operational_dir, fact_name=icell_fact, genelist=ICELL_GENELIST_FILENAME, output_filename=ICELL_FILENAME)
        data = json.dumps({
        'msg': "Successfully computed icell",
        # 'icell_img': icell_img[0],
        })
        return HttpResponse(data)
    except Exception as e:
        LOGGER.error(e)
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)

def compute_gdvs(request):
    print("start compute_gdvs")
    try:
        print("request.POST", request.POST)
        print("request.FILES", request.FILES)
        data = json.loads(request.POST["data"])
        icell_tasks = data["icell_tasks"]
        for task_id in icell_tasks:
            task = get_task_with_id(task_id)
            task_dir = task.operational_directory
            operational_dir = COMPUTATIONS_DIR + "/" + task_dir
            LOGGER.info("Executing GDV for task: " + str(task_id) + " in dir: " + str(task_dir))
            compute_gdv_for_icell(op_dir=operational_dir, file_name=ICELL_FILENAME)
        completed_tasks_gdv = get_all_gdv_successful_tasks_for_user(task_type=DATA_FUSION_TASK, user=request.user)
        print("completed_tasks_gdv", completed_tasks_gdv)
        data = json.dumps({
        'msg': "Successfully computed gdvs",
        'completed_tasks_gdv': completed_tasks_gdv
        })
        return HttpResponse(data)
    except Exception as e:
        LOGGER.error(e)
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)

def compute_gdv_sims(request):
    print("start compute_gdv_sims")
    try:
        print("request.POST", request.POST)
        print("request.FILES", request.FILES)
        print("request.FILES['genelist']", request.FILES["genelist"])
        data = json.loads(request.POST["data"])
        icell_tasks = data["gdv_tasks"]
        gdv_files = []
        for task_id in icell_tasks:
            task = get_task_with_id(task_id)
            task_dir = task.operational_directory
            # gdv_files.append(COMPUTATIONS_DIR + "/" + task_dir + "/" + ICELL_GDV_FILE_NAME)
            gdv_files.append(task_dir)
        print("gdv_files", gdv_files)
        operational_dir = COMPUTATIONS_DIR + "/" + GDV_SIMS_COMP_FOLDER
        LOGGER.info("Executing GDV for task: " + str(task_id) + " in dir: " + str(task_dir))
        # result = make_system_call("rm -rf " + operational_dir + "/*", working_dir=operational_dir)
        result = make_system_call("rm -rf " + operational_dir)
        # print("result", result)
        result = make_system_call("mkdir " + operational_dir)
        # print("result", result)
        save_file_to_dir(operational_dir, GDV_GENELIST_FILENAME, request.FILES["genelist"])
        compute_gdv_similarities(op_dir=operational_dir, genelist=GDV_GENELIST_FILENAME, gdv_filenames=gdv_files, output_filename=GDV_SIMS_FILENAME)
        # ---
        # completed_tasks_gdv = get_all_gdv_successful_tasks_for_user(task_type=DATA_FUSION_TASK, user=request.user)
        # print("completed_tasks_gdv", completed_tasks_gdv)
        with open(operational_dir + "/" + GDV_SIMS_FILENAME, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            # gdv_sims = list(reader)
            gdv_sims = []
            for i,row in enumerate(reader):
                gdv_sims.append((row[0], row[1]))
                # print(row)
                # print(row[0].split())
        print("gdv_sims", gdv_sims)
        gdv_sims = sorted(gdv_sims, key=lambda tup: tup[1], reverse=False)
        print("gdv_sims", gdv_sims)
        if len(gdv_sims) > 100:
            gdv_sims = gdv_sims[0:100]
        print("gdv_sims", gdv_sims)

                # if(i >= 9):
                #     break
        
        data = json.dumps({
        'msg': "Successfully computed gdvs",
        # 'completed_tasks_gdv': completed_tasks_gdv
        'gdv_sims': gdv_sims
        })
        return HttpResponse(data)
    except Exception as e:
        LOGGER.error(e)
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)

def save_file_to_dir(directory, filename, filedata):
    print("save_file_to_dir for file:", filename)
    print("result_remove_file", make_system_call("rm -f " + directory + "/" + filename))
    blob = filedata
    print("blob", blob)
    # print("blob.read()", blob.read())
    # print("blob.read()", blob.read())
    fs = FileSystemStorage(directory) #defaults to   MEDIA_ROOT  
    filename_res = fs.save(filename, ContentFile(blob.read()))
    print("filename_res", filename_res)

def delete_data_for_task(task):
    operational_dir = COMPUTATIONS_DIR + "/" + task.operational_directory
    if os.path.exists(operational_dir):
        result = make_system_call("rm -r " + operational_dir)
        return result.return_code == 0
    return True

def get_view_for_task(task, user):
    facts, output_files, extra_res = get_all_results(task=task)
    context = Context({
        'facts': facts,
        'output_files': output_files,
        'extra_res': extra_res,
        'task': task,
    })
    return HttpResponse(get_template("DataFusion/result.html").render(context))

def delete_data_for_task(task):
    operational_dir = COMPUTATIONS_DIR + "/" + task.operational_directory
    if os.path.exists(operational_dir):
        result = make_system_call("rm -r " + operational_dir)
        return result.return_code == 0
    return False

def get_raw_data_for_task(task):
    return get_all_downloadable_results(task)

def get_view_for_result_icell_analysis(request): 
    completed_tasks_icell, completed_tasks_gdv = get_all_icell_successful_tasks_for_user(task_type=DATA_FUSION_TASK, user=request.user)
    # print("completed_tasks_icell:", completed_tasks_icell)
    # print("completed_tasks_gdv", completed_tasks_gdv)
    context = Context({
        'completed_tasks_icell': completed_tasks_icell,
        'completed_tasks_gdv': completed_tasks_gdv,
    })
    # return HttpResponse("")
    return HttpResponse(get_template("DataFusion/result_icell_analysis.html").render(context))

def get_task_view_psb(request, task_id):
    task = get_task_with_id(task_id=task_id)
    if task:
        LOGGER.info("Rending psb options for Task: " + str(task) + " in dir: " + task.operational_directory)
        if task.error_occurred:
            return HttpResponse(
                get_template("dashboard/error_result.html").render(Context({
                    'error_text': task.error_text
                })))
        return get_task_view_psb_render(task=task, user=request.user)
    LOGGER.error("Invalid Task ID received for viewing psb options.")
    return HttpResponseBadRequest("Task ID is incorrect.")

def get_task_view_psb_render(task, user):
    facts, output_files, extra_res = get_all_results(task=task)
    print("facts", facts)
    context = Context({
        'facts': facts,
        'output_files': output_files,
        'extra_res': extra_res,
        'task': task,
    })
    return HttpResponse(get_template("DataFusion/result_psb_analysis.html").render(context))

# ---------------------------------
# tasks related functions

from TaskFactory.models import Task
def get_all_icell_successful_tasks_for_user(task_type, user):
    tasks_icell, tasks_gdv = [], []
    for t in Task.objects.filter(user=user, task_type=task_type, finished=True, error_occurred=False):
        fnames = os.listdir(COMPUTATIONS_DIR + "/" + t.operational_directory)
        # print("fnames", fnames)
        if any(ICELL_FILENAME in fname for fname in fnames):
            tasks_icell.append((t.taskId, t.taskName))
            # print("fnames", fnames)
            if any(ICELL_GDV_FILENAME in fname for fname in fnames):
                tasks_gdv.append((t.taskId, t.taskName))
    return tasks_icell, tasks_gdv

def get_all_gdv_successful_tasks_for_user(task_type, user):
    tasks_gdv = []
    for t in Task.objects.filter(user=user, task_type=task_type, finished=True, error_occurred=False):
        fnames = os.listdir(COMPUTATIONS_DIR + "/" + t.operational_directory)
        if any(ICELL_GDV_FILENAME in fname for fname in fnames):
            tasks_gdv.append((t.taskId, t.taskName))
    return tasks_gdv

def get_task_with_id(task_id):
    return Task.objects.get(taskId=task_id)

