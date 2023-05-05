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
import numpy as np
import matplotlib.pyplot as plt
import unicodedata
from .settings import *
from utils.SystemCall import make_system_call
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage, FileSystemStorage
from PIL import Image
import base64
import StringIO
import io
from django.shortcuts import render
import ast
from django.template.response import TemplateResponse

LOGGER = logging.getLogger(__name__)

# ---------------------------------------------

@login_required
@ajax_required
def update_drugstone_container(request):
    print("start update_drugstone_container")
    drugstone_settings = {
        'groups': json.dumps({'nodeGroups': {'Gene': {'type':'Gene','color':'#999999','groupName':'Genes','shape':'ellipse'}}}),
        'config': json.dumps({'identifier': 'symbol', 'title': 'GraphFusion + DrugstOne', 'autofillEdges': True}),
        'network': []
    }
    try:
        # print("request.POST", request.POST)
        # print("request.FILES", request.FILES)
        data = json.loads(request.POST["data"])
        # get clusters from data
        clusters = data["clusters"]
        clusters = unicodedata.normalize('NFKD', clusters).encode('ascii', 'ignore')
        clusters = ast.literal_eval(clusters)
        # print("clusters", clusters)
        # get cluster ids
        cluster_ids = list(map(int, data["cluster_ids"]))
        print("cluster_ids", cluster_ids)
        # prepare nodes
        # genes = clusters[cluster_ids[0]]
        # genes = [entity for cluster in clusters[cluster_ids] for entity in cluster]
        genes = []
        for id in cluster_ids:
            genes += clusters[id]
        print("genes", genes)
        nodes = [{'id':gene, 'group': 'Gene'} for gene in genes]
        drugstone_settings['network'] = json.dumps({'nodes': nodes})
        return render(request, 'ClusteringAndEnrichment/clusteringAndEnrichmentAnalysis/drugstone_container.html', drugstone_settings)
    except Exception as e:
        LOGGER.error(e)
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)

# ---------------------------------------------

@login_required
@ajax_required
def analysis_page(request):
    context = Context({})

    # test using drugstone
    drugstone_settings = {
        'config': {"title": "GraphFusion + DrugstOne"},
        'network': {"nodes": []}
    }

    # clusters = [['MYC', 'PTGES3', 'HCFC1', 'BRCA1', 'HTT', 'BRCA2'], ['EED', 'WT1', 'RPL5', 'NRAS', 'FLT3'], ['IDH2', 'TUBA1A', 'PTEN', 'RAG2'], ['MAGEC3',  'CREBBP', 'NXF1'], ['TRIM25', 'ASXL1']]
    # context['clusters'] = clusters
    # genes = clusters[0]
    # genes = []
    # nodes = [{'id':gene, 'group': 'Gene'} for gene in genes]
    # drugstone_settings['network'] = json.dumps({'nodes': nodes})
    context.update(drugstone_settings)

    # print("context", context)
    return HttpResponse(get_template("ClusteringAndEnrichment/clusteringAndEnrichmentAnalysis/analysis.html").render(context))

@login_required
@ajax_required
def visualise_factor(request):
    print("visualise_factor")
    try:
        # print("request.POST", request.POST)
        print("request.FILES", request.FILES)
        data = json.loads(request.POST["data"])
        cluster_fact = data["cluster_fact"]
        cluster_fact_name = unicodedata.normalize('NFKD', cluster_fact[0]).encode('ascii', 'ignore')
        cluster_fact_data = unicodedata.normalize('NFKD', cluster_fact[1]).encode('ascii', 'ignore')
        operational_dir = COMPUTATIONS_DIR + "/clustering_enrichment"
        # empty computations directory
        make_system_call("rm -r " + operational_dir)
        make_system_call("mkdir " + operational_dir)
        # save cluster_fact_data to file
        _save_text_file_to_dir(operational_dir, cluster_fact_name, cluster_fact_data)
        # example of plotting a heatmap using cluster_fact_data
        path_to_csv= operational_dir + "/" + cluster_fact_name
        heatmap_data = np.genfromtxt(path_to_csv) #, delimiter='\t'
        fig, ax = plt.subplots()
        heatmap = ax.pcolor(heatmap_data, cmap=plt.cm.Blues)
        # set the limits of the plot to the lenght of the data
        ax.set_xlim(0, heatmap_data.shape[1])
        ax.set_ylim(0, heatmap_data.shape[0])
        # want a more natural, table-like display
        '''By convention, heatmaps tend to reverse the y-axis because it allows the plot to be consistent with the way that matrices are typically displayed in mathematics and computer science. In these fields, the convention is to place the origin (i.e., (0, 0)) in the upper-left corner of the matrix, with the x-axis running from left to right and the y-axis running from top to bottom.'''
        ax.invert_yaxis()
        ax.xaxis.tick_top()
        # set the plot title
        # ax.set_title("Factor heatmap", y=1.05)
        # set x and y axis titles
        ax.set_xlabel("Dimensions of each entity")
        ax.set_ylabel("Entities")
        # include the side colorbar with the legend
        plt.colorbar(heatmap)
        # add a title to the colorbar
        # plt.title("Heatmap of the factor")
        # encode the plot as a base64 string
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        # prepare response
        data = json.dumps({
        'msg': "Successfully plotted factor",
        'factor_img': '{0}'.format(b64),
        })
        return HttpResponse(data)
    except Exception as e:
        LOGGER.error(e)
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)

@login_required
@ajax_required
def compute_clusters(request):
    print("start compute_clusters")
    try:
        # print("request.POST", request.POST)
        # print("request.FILES", request.FILES)
        data = json.loads(request.POST["data"])
        cluster_fact = data["cluster_fact"]
        cluster_fact_name = unicodedata.normalize('NFKD', cluster_fact[0]).encode('ascii', 'ignore')
        # cluster_fact_data = unicodedata.normalize('NFKD', cluster_fact[1]).encode('ascii', 'ignore')
        operational_dir = COMPUTATIONS_DIR + "/clustering_enrichment"
        LOGGER.info("Executing clustering for fact: " + str(cluster_fact_name) + " in dir: " + operational_dir)
        # _save_text_file_to_dir(operational_dir, cluster_fact_name, cluster_fact_data)
        _save_blob_file_to_dir(operational_dir, CLUSTERS_ENTITYLIST_FILENAME, request.FILES["clusters_entitylist_file"])
        if os.path.isfile(os.path.join(operational_dir, CLUSTERS_ENTITYLIST_FILENAME)):
            entities = np.genfromtxt(os.path.join(operational_dir, CLUSTERS_ENTITYLIST_FILENAME), dtype=str)
            factor = np.genfromtxt(os.path.join(operational_dir, cluster_fact_name))
            if entities.shape[0] -1 != factor.shape[0]:
                print("entities.shape", entities.shape)
                print("factor.shape", factor.shape)
                raise Exception("Number of entities in entitylist file (+header): {}, does not match number of rows in factor file: {}".format(entities.shape[0],factor.shape[0]))  
        clusters_img, clusters = _compute_clusters_for_factor(op_dir=operational_dir, fact_name=cluster_fact_name)
        data = json.dumps({
        'msg': "Successfully computed clusters",
        'clusters_img': clusters_img[0],
        'clusters': clusters,
        })
        return HttpResponse(data)

    except Exception as e:
        LOGGER.error(e)
        print("error", e)
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)

@login_required
@ajax_required
def compute_enrichments(request):
    print("start compute_enrichments")
    try:
        print("request.POST", request.POST)
        print("request.FILES", request.FILES)
        data = json.loads(request.POST["data"])
        cluster_fact = data["cluster_fact"]
        # enrichments_anno = data["enrichments_anno"]
        # enrichments_anno = "iCell" # TODO REMOVE
        # task_dir = data["task_dir"]
        operational_dir = COMPUTATIONS_DIR + "/clustering_enrichment"
        LOGGER.info("Executing enrichments for fact: " + str(cluster_fact) + " and annotations in dir: " + operational_dir)
        _save_blob_file_to_dir(operational_dir, ENRICHMENTS_ANNO_FILENAME, request.FILES["annotations"])
        enrichments_img, clusters_enriched = _compute_enrichments_for_clusters(op_dir=operational_dir, fact_name=cluster_fact, enrichments_anno=ENRICHMENTS_ANNO_FILENAME)
        data = json.dumps({
        'msg': "Successfully computed enrichments",
        'enrichments_img': enrichments_img[0],
        'clusters_enriched': clusters_enriched,
        })
        return HttpResponse(data)
    except Exception as e:
        LOGGER.error(e)
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)

# ------------------ internal methods ------------------
def _compute_clusters_for_factor(op_dir, fact_name):
    sys_call_result = make_system_call("bash " + CLUSTERS_SCRIPT_PATH + " " + op_dir + " " + fact_name + " " + CLUSTERS_ENTITYLIST_FILENAME, working_dir=op_dir)
    print("sys_call_result", sys_call_result)
    clusters_img = []
    if os.path.isfile(os.path.join(op_dir, "clusters_from_factor.png")):
        clusters_img.append('{0}'.format(_get_string_for_png(os.path.join(op_dir, "clusters_from_factor.png"))))
    # load numpy array from file
    # clusters = np.load(os.path.join(op_dir, "clusters.npy"), allow_pickle=True)
    # import numpy.lib.npyio as npyio
    # clusters = npyio.load(os.path.join(op_dir, "clusters.npy"))
    # print("clusters", clusters)
    # facts = pickle.load(open("./facts.pkl", "rb"))
    # read list of lists from csv file
    with open(os.path.join(op_dir, "clusters.csv"), 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        clusters = list(reader)
        # print("clusters", clusters)
    return clusters_img, clusters

def _compute_enrichments_for_clusters(op_dir, fact_name, enrichments_anno):
    sys_call_result = make_system_call("bash " + ENRICHMENTS_SCRIPT_PATH + " " + op_dir + " " + fact_name + " " + CLUSTERS_ENTITYLIST_FILENAME + " " + enrichments_anno, working_dir=op_dir)
    print("sys_call_result", sys_call_result)
    clusters_img = []
    if os.path.isfile(os.path.join(op_dir, "enrichments_for_clusters.png")):
        clusters_img.append('{0}'.format(_get_string_for_png(os.path.join(op_dir, "enrichments_for_clusters.png"))))
    with open(os.path.join(op_dir, "clusters_enriched.csv"), 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        clusters_enriched = list(reader)
        # print("clusters_enriched", clusters_enriched)
    return clusters_img, clusters_enriched

def _save_text_file_to_dir(directory, filename, filedata):
    print("_save_text_file_to_dir for file:", filename)
    edgelist_path = directory + "/" + filename
    f = open(edgelist_path, "w")
    f.write(filedata)
    f.close()

def _save_blob_file_to_dir(directory, filename, filedata):
    print("_save_blob_file_to_dir for file:", filename)
    sys_call_result = make_system_call("rm -f " + directory + "/" + filename)
    print("sys_call_result", sys_call_result)
    blob = filedata
    fs = FileSystemStorage(directory) #defaults to   MEDIA_ROOT  
    filename_res = fs.save(filename, ContentFile(blob.read()))
    print("filename_res", filename_res)
    
def _get_string_for_png(file_path):
    output = StringIO.StringIO()
    im = Image.open(file_path)
    im.save(output, format='PNG')
    output.seek(0)
    output_s = output.read()
    b64 = base64.b64encode(output_s)
    return '{0}'.format(b64)