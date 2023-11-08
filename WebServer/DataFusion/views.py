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
from .settings import *
from utils.SystemCall import make_system_call
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage, FileSystemStorage
from .DataFusionAnalysisResult import *
from utils.InputFormatter import check_input_format, check_column_list_format

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

def _get_factor_shape(request_FILES, fact_name):
    factor = request_FILES[fact_name].read().decode("utf-8")
    request_FILES[fact_name].seek(0)
    n_rows = len([row for row in factor.split("\n") if len(row) > 0])
    first_row = factor.split("\n")[0]
    n_cols = 0
    if "\t" in first_row:
        n_cols = len(factor.split("\n")[0].split("\t"))
    elif "," in first_row:
        n_cols = len(factor.split("\n")[0].split(","))
    elif " " in first_row:
        n_cols = len(factor.split("\n")[0].split(" "))
    return n_rows, n_cols

def _check_input(max_iter, delta_min, facts, request_FILES):
    if int(max_iter) <= 0:
        return HttpResponseBadRequest("Invalid max_iter")
    if float(delta_min) <= 0:
        return HttpResponseBadRequest("Invalid delta_min")
    factorization_shapes = []
    for fact in facts:
        print("-"*50); print("fact", fact)
        counter = fact["counter"]
        if fact["factType"] not in [x[0] for x in FACTORIZATION_TYPE[1:]]:
            return HttpResponseBadRequest("Invalid 'Type of factorization' in row " + str(counter))
        if fact["initType"] not in [x[0] for x in FACTOR_INIT_TYPE]:
            return HttpResponseBadRequest("Invalid 'Type of initialization' in row " + str(counter))
        if "M0" not in fact.keys() or len(fact["M0"]) == 0 or fact["M0"] not in request_FILES.keys():
            return HttpResponseBadRequest("Invalid factor/network (M0) in row " + str(counter))
        ks = fact["M2Ks"]
        if ks is None or len(ks) == 0:
            return HttpResponseBadRequest("Invalid ks in row " + str(counter))
        else:
            # Split ks by spaces or commas depending on the input
            ks = ks.split(",") if "," in ks else ks.split()
            for k in ks:
                if int(k) <= 0:
                    return HttpResponseBadRequest("Invalid ks in row " + str(counter))
        # Check if the Ks are correct for the given factorization type and factor size
        # m = factor_rows, n = factor_cols
        m, n = _get_factor_shape(request_FILES, fact["M0"])
        X_shape = (m, n)
        print("X_shape", X_shape)
        # Check the Ks for the given factorization type
        if fact["factType"] == FACTORIZATION_TYPE[1][0]:    # NMF
            # NMF decomposes a rectangular matrix X E Rm*n in the product of positive factors F E R+ m*k and G E R+ n*k two, with k <= min(m, n), such that ||X-F*GT||F^2 is minimized.
            if len(ks) != 1:
                return HttpResponseBadRequest("Invalid ks in row " + str(counter) + ". For '" + FACTORIZATION_TYPE[1][1] + "', only one k is allowed.")
            if int(ks[0]) > min(m, n):
                return HttpResponseBadRequest("Invalid ks in row " + str(counter) + ". For '" + FACTORIZATION_TYPE[1][1] + "', k must be <= min(m, n). Input factor has " + str(m) + " rows and " + str(n) + " columns.")
            # min||X-F*GT||
            F_shape = (m, int(ks[0]))
            G_shape = (n, int(ks[0]))
            factorization_shapes.append((X_shape, F_shape, None, G_shape))
        elif fact["factType"] == FACTORIZATION_TYPE[2][0]:  # NMTF
            # NMTF decomposes a rectangular matrix X E Rm*n in the product of three positive factors F E R+ m*k 1 , S E R+ k1 *k2 and G E R+ n*k2 , with k1, k2 <= min(m, n), such that ||X-F*S*GT||F^2 is minimized.
            if len(ks) != 2:
                return HttpResponseBadRequest("Invalid ks in row " + str(counter) + ". For '" + FACTORIZATION_TYPE[2][1] + "', two ks are required.")
            if int(ks[0]) > min(m, n) or int(ks[1]) > min(m, n):
                return HttpResponseBadRequest("Invalid ks in row " + str(counter) + ". For '" + FACTORIZATION_TYPE[2][1] + "', k1 and k2 must be <= min(m, n). Input factor has " + str(m) + " rows and " + str(n) + " columns.")
            # min||X-F*S*GT||F^2
            F_shape = (m, int(ks[0]))
            S_shape = (int(ks[0]), int(ks[1]))
            G_shape = (n, int(ks[1]))
            factorization_shapes.append((X_shape, F_shape, S_shape, G_shape))
        elif fact["factType"] == FACTORIZATION_TYPE[3][0]:  # SNMF
            # SNMF decomposes a symmetric matrix X E Rn*n in the product of two positive factors G E Rn*k +, with k <= n, such that ||X-G*GT||F^2 is minimized.
            if m != n:
                return HttpResponseBadRequest("Invalid input factor in row " + str(counter) + ". For '" + FACTORIZATION_TYPE[3][1] + "', the factor must be square. Input factor has " + str(m) + " rows and " + str(n) + " columns.")
            if len(ks) != 1:
                return HttpResponseBadRequest("Invalid ks in row " + str(counter) + ". For '" + FACTORIZATION_TYPE[3][1] + "', only one k is allowed.")
            if int(ks[0]) > n:
                return HttpResponseBadRequest("Invalid ks in row " + str(counter) + ". For '" + FACTORIZATION_TYPE[3][1] + "', k must be <= n. Input factor has " + str(m) + " rows and " + str(n) + " columns.")
            # min||X-G*GT||F^2
            G_shape = (m, int(ks[0]))
            factorization_shapes.append((X_shape, None, None, G_shape))
        elif fact["factType"] == FACTORIZATION_TYPE[4][0]:  # SNMTF
            # SNMTF decomposes a symmetric matrix X E Rn*n in the product of two positive factors G E R+ n*k and S E R+ k*k , with k <= n, such that ||X-G*S*GT||F^2 is minimized.
            if m != n:
                return HttpResponseBadRequest("Invalid input factor in row " + str(counter) + ". For '" + FACTORIZATION_TYPE[4][1] + "', the factor must be square. Input factor has " + str(m) + " rows and " + str(n) + " columns.")
            if len(ks) != 2:
                return HttpResponseBadRequest("Invalid ks in row " + str(counter) + ". For '" + FACTORIZATION_TYPE[4][1] + "', two ks are required.")
            if int(ks[0]) > n or int(ks[1]) > n:
                return HttpResponseBadRequest("Invalid ks in row " + str(counter) + ". For '" + FACTORIZATION_TYPE[4][1] + "', k1 and k2 must be <= n. Input factor has " + str(m) + " rows and " + str(n) + " columns.")
            # min||X-G*S*GT||F^2
            G_shape = (m, int(ks[0]))
            S_shape = (int(ks[0]), int(ks[1]))
            factorization_shapes.append((X_shape, None, S_shape, G_shape))
        # Check the shape of the contraint factors if present
        if "M1C" in fact.keys() and len(fact["M1C"]) > 0:
            # Get size of the constraint matrix
            M1C_shape = _get_factor_shape(request_FILES, fact["M1C"])
            print("M1C_shape", M1C_shape)
            # Check that the constraint matrix has the correct size
            if M1C_shape != (m, m):
                return HttpResponseBadRequest("Invalid constraint matrix in row " + str(counter) + ". For '" + FACTORIZATION_TYPE[1][1] + "', the constraint matrix must be square and have the same number of rows as the input factor. Input factor has " + str(m) + " rows and " + str(n) + " columns. Constraint matrix has " + str(M1C_shape[0]) + " rows and " + str(M1C_shape[1]) + " columns.")
        if "M3C" in fact.keys() and len(fact["M3C"]) > 0:
            # Get size of the constraint matrix
            M3C_shape = _get_factor_shape(request_FILES, fact["M3C"])
            print("M3C_shape", M3C_shape)
            # Check that the constraint matrix has the correct size
            if M3C_shape != (n, n):
                return HttpResponseBadRequest("Invalid constraint matrix in row " + str(counter) + ". For '" + FACTORIZATION_TYPE[1][1] + "', the constraint matrix must be square and have the same number of columns as the input factor. Input factor has " + str(m) + " rows and " + str(n) + " columns. Constraint matrix has " + str(M3C_shape[0]) + " rows and " + str(M3C_shape[1]) + " columns.")
    # Check the shape of the shared factors if present
    fact_sharings = []
    up, down, updown = FACTOR_SHARE_DIRECTION[1][0], FACTOR_SHARE_DIRECTION[2][0], FACTOR_SHARE_DIRECTION[3][0]
    for fact in facts:
        M1S = ""
        if "M1S" in fact.keys() and len(fact["M1S"]) > 0:
            M1S = fact["M1S"]
            print("M1S", M1S)
        M3S = ""
        if "M3S" in fact.keys() and len(fact["M3S"]) > 0:
            M3S = fact["M3S"]
            print("M3S", M3S)
        fact_sharings.append((M1S, M3S))
    print("fact_sharing", fact_sharings)
    # Check that the shared factors are correct.
    for i, (M1S, M3S) in enumerate(fact_sharings):
        # Don't allow sharing of both factors M1S and M3S in the same direction
        if (M1S == up or M1S == updown) and (M3S == up or M3S == updown):
            return HttpResponseBadRequest("Invalid shared factor in row " + str(i) + ". Cannot share both factors in the same direction.")
        if (M1S == down or M1S == updown) and (M3S == down or M3S == updown):
            return HttpResponseBadRequest("Invalid shared factor in row " + str(i) + ". Cannot share both factors in the same direction.")
        # Don't allow the first row to share factors in the up or updown direction
        if i == 0 and (M1S == up or M1S == updown or M3S == up or M3S == updown):
            return HttpResponseBadRequest("Invalid shared factor in row " + str(i) + ". Cannot share factors in the upwards or upwards+downwards direction in the first row.")
        # Don't allow the last row to share factors in the down or updown direction
        if i == len(fact_sharings) - 1 and (M1S == down or M1S == updown or M3S == down or M3S == updown):
            return HttpResponseBadRequest("Invalid shared factor in row " + str(i) + ". Cannot share factors in the downwards or upwards+downwards direction in the last row.")
        # Check that the shared factors have the correct size. It means that the number of columns of the factor shared downwards must be equal to the number of rows of the factor shared upwards in the next row.
        downwards_shape, upwards_shape = None, None
        if M1S == down or M1S == updown:
            downwards_shape = factorization_shapes[i][1]
        elif M3S == down or M3S == updown:
            downwards_shape = factorization_shapes[i][3]
        if downwards_shape is not None:
            if fact_sharings[i+1][0] == up or fact_sharings[i+1][0] == updown:
                upwards_shape = factorization_shapes[i+1][1]
            elif fact_sharings[i+1][1] == up or fact_sharings[i+1][1] == updown:
                upwards_shape = factorization_shapes[i+1][3]
            if upwards_shape is None:
                return HttpResponseBadRequest("Invalid shared factor in row " + str(i) + ". Cannot share factors in the downwards or upwards+downwards direction if the next row does not share factors in the upwards or upwards+downwards direction.")
        # print("downwards_shape", downwards_shape)
        # print("upwards_shape", upwards_shape)
        # print("fact_sharings", fact_sharings)
        if downwards_shape is not None and upwards_shape is not None and (downwards_shape[0] != upwards_shape[0] or downwards_shape[1] != upwards_shape[1]):
            return HttpResponseBadRequest("Invalid shared factor in row " + str(i) + ". The shape of the factor shared downwards must be equal to the shape of the factor shared upwards in the next row. Factor shared downwards has shape " + str(downwards_shape) + ". Factor shared upwards has shape " + str(upwards_shape) + ".")
        # Check if there is any missmatched upwards sharing
        if (M1S == up or M1S == updown or M3S == up or M3S == updown) and (fact_sharings[i-1][0] != down and fact_sharings[i-1][0] != updown and fact_sharings[i-1][1] != down and fact_sharings[i-1][1] != updown):
            return HttpResponseBadRequest("Invalid shared factor in row " + str(i) + ". Cannot share factors in the upwards or upwards+downwards direction if the previous row does not share factors in the downwards or upwards+downwards direction.")
    LOGGER.info("All input checks passed")
    return False

# from django.views.decorators.http import require_POST
# @require_POST
@login_required
@ajax_required
# @csrf_exempt
def submit_analysis(request):
    # print("start submit_analysis")
    try:
        # print("request.POST", request.POST)
        # print("request.FILES", request.FILES)        
        data = json.loads(request.POST["data"])
        facts = data["facts"]
        task_name = data["task_name"]
        setup = data["setup"]
        net_names = data["net_names"]
        max_iter = data["max_iter"]
        delta_min = data["delta_min"]
        # print("facts", facts)
        # print("task_name", task_name)
        # print("setup", setup)
        # print("net_names", net_names)
        # print("max_iter", max_iter)
        # print("delta_min", delta_min)
        # vvvvvvvvvvvvvvvvvvvvvvvvvvv
        # Check the input networks/factors
        for net_name in net_names:
            # If network name is not present in the facts, skip it
            if net_name not in [value for fact in facts for value in fact.values()]:
                continue
            network = [net_name, request.FILES[net_name].read().decode("utf-8")]
            # print("network[0]", network[0])
            check_response, network[1] = check_input_format(network[1], input_task_or_type='factor', verbose=False)
            if not check_response:
                err_msg = "Error: Incorrect format in input file '" + network[0] + "'. " + (network[1] if network[1] is not None else "")
                return HttpResponseBadRequest(err_msg)
            request.FILES[net_name] = ContentFile(network[1].encode("utf-8"))
        # Check the input parameters
        check_input_res = _check_input(max_iter, delta_min, facts, request.FILES)
        if check_input_res:
            return check_input_res
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^
        LOGGER.info("Executing DataFusionAnalysis for: " + str(request.user.username) + " with task_name: " + str(task_name))
        request_FILES = request.FILES
        task = DataFusionAnalysis(facts, net_names, request_FILES, task_name=task_name, setup=setup, user=request.user, max_iter=max_iter, delta_min=delta_min)
        task.submit()
        return HttpResponse("Successfully submitted task " + task_name)
    except Exception as e:
        LOGGER.error(e)
        return HttpResponseBadRequest(e.message)

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

def _compute_clusters_check_input(operational_dir, fact_name, request_FILES, request_filename):
    print("_compute_clusters_check_input")
    # Read cluster_fact from file
    file_path = operational_dir + "/" + fact_name
    # Read whole file a string
    try:
        with open(file_path, 'r') as f:
            fact_str = f.read()    
    except Exception as e:
        return HttpResponseBadRequest("Error: Incorrect format in input file " + fact_name)
    check_response, fact_str = check_input_format(fact_str, input_task_or_type='factor', verbose=False)
    # Check input file format
    if not check_response:
        err_msg = "Error: Incorrect format in input file '" + fact_name + "'. " + (fact_str if fact_str is not None else "")
        return HttpResponseBadRequest(err_msg)
    # Check the entity list file format
    check_response, entities = check_input_format(request_FILES[request_filename].read().decode("utf-8"), input_task_or_type='entitylist', verbose=False)
    if not check_response:
        return HttpResponseBadRequest("Error occurred while processing 'entity list' file. " + str(entities) + ".")
    request_FILES[request_filename].seek(0)
    # Check that the number of rows in the entity list file is the same as the number of rows in the cluster fact
    if len(entities.split("\n")) != len(fact_str.split("\n")):
        return HttpResponseBadRequest("Error: The number of rows in the entity list file must be the same as the number of rows in the cluster fact. Entity list has " + str(len(entities.split("\n"))) + " rows. Cluster fact has " + str(len(fact_str.split("\n"))) + " rows.")
    return False

def compute_clusters(request):
    print("start compute_clusters")
    try:
        print("request.POST", request.POST)
        print("request.FILES", request.FILES)
        data = json.loads(request.POST["data"])
        cluster_fact = data["cluster_fact"]
        task_dir = data["task_dir"]
        operational_dir = COMPUTATIONS_DIR + "/" + task_dir
        # Check input for clustering
        check_input_res = _compute_clusters_check_input(operational_dir, cluster_fact, request.FILES, "clusters_entitylist_file")
        if check_input_res:
            return check_input_res
        # Excute clustering
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
        return HttpResponseBadRequest(e.message)

def _compute_enrichments_check_input(request_FILES):
    print("_compute_enrichments_check_input")
    # Check the annotations file format
    check_response, annotations = check_input_format(request_FILES["annotations"].read().decode("utf-8"), input_task_or_type='entityanno', verbose=False) # type: ignore
    if not check_response:
        return HttpResponseBadRequest("Error occurred while processing 'annotations' file. " + str(annotations) + ".")
    request_FILES["annotations"].seek(0)
    return False

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
        # Check input for clustering in case of any change
        # check_input_res = _compute_clusters_check_input(operational_dir, cluster_fact, request.FILES, "clusters_entitylist_file")
        # if check_input_res:
        #     return check_input_res
        # Check input for enrichments
        check_input_res = _compute_enrichments_check_input(request.FILES)
        if check_input_res:
            return check_input_res
        # Excute enrichments
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
        # Check input for icell
        check_input_res = _compute_clusters_check_input(operational_dir, icell_fact, request.FILES, "genelist")
        if check_input_res:
            return check_input_res
        # print("result_make_system_call", make_system_call("rm " + operational_dir + "/" + ICELL_FILENAME))
        # return HttpResponseBadRequest("No errors found. Not ready yet.")
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

def _compute_gdv_sims_check_input(data, icell_tasks, request_FILES, gdv_files):
    print("_compute_gdv_sims_check_input")
    # Check that genelist is present
    if "genelist" not in request_FILES.keys():
        return HttpResponseBadRequest("Error: No genelist file found.")
    # Check the entity list file format
    check_response, entities = check_input_format(request_FILES["genelist"].read().decode("utf-8"), input_task_or_type='entitylist', verbose=False)
    if not check_response:
        return HttpResponseBadRequest("Error occurred while processing 'entity list' file. " + str(entities) + ".")
    request_FILES["genelist"].seek(0)
    # Get entities as a list
    entities = entities.split("\n")
    # Get unique entities
    entities = list(set(entities))
    # print("entities", entities)
    # Get the entities from all the gdv files. They're in the first column
    gdv_entities = []
    for gdv_file in gdv_files:
        with open(COMPUTATIONS_DIR + "/" + gdv_file + "/" + ICELL_GDV_FILENAME, 'rb') as f:
            reader = csv.reader(f, delimiter=' ')
            for i,row in enumerate(reader):
                # print("row", row)
                gdv_entities.append(row[0])
    # Get unique entities
    gdv_entities = list(set(gdv_entities))
    # print("gdv_entities", gdv_entities)
    # Check that gdv_entities are a subset of entities
    if not set(gdv_entities).issubset(set(entities)):
        # Print the entities that are in gdv_entities but not in entities
        # print("gdv_entities", gdv_entities)
        # print("entities", entities)
        print("set(gdv_entities).difference(set(entities))", set(gdv_entities).difference(set(entities)))
        return HttpResponseBadRequest("Error: The entities in the genelist file must be a subset of the entities in the gdv files.")
    # return HttpResponseBadRequest("No errors found. Not ready yet.")
    return False
    

def compute_gdv_sims(request):
    print("start compute_gdv_sims")
    try:
        # print("request.POST", request.POST)
        # print("request.FILES", request.FILES)
        data = json.loads(request.POST["data"])
        icell_tasks = data["gdv_tasks"]
        gdv_files = []
        for task_id in icell_tasks:
            task = get_task_with_id(task_id)
            task_dir = task.operational_directory
            # gdv_files.append(COMPUTATIONS_DIR + "/" + task_dir + "/" + ICELL_GDV_FILE_NAME)
            gdv_files.append(task_dir)
        # Check input for gdv_sims
        check_input_res = _compute_gdv_sims_check_input(data, icell_tasks, request.FILES, gdv_files)
        if check_input_res:
            return check_input_res
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
        return HttpResponseBadRequest(e.message)

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

