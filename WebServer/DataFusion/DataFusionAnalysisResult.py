__author__ = 'carlos garcia-hernandez'

import os
import pickle
from fnmatch import fnmatch
# import h5py
import numpy as np
import logging
from PIL import Image
import base64
import StringIO

from django.template import Context
from django.template.loader import get_template
from .settings import * 
from utils.SystemCall import make_system_call

LOGGER = logging.getLogger(__name__)

def compute_psb_matcomp_for_factor(op_dir, fact_name):
    sys_call_result = make_system_call("bash " + PSB_MATCOMP_SCRIPT_PATH + " " + op_dir + " " + fact_name + " " + PSB_MATCOMP_OUT_FILES[0] + " " + PSB_MATCOMP_OUT_FILES[1] + " " + PSB_MATCOMP_ENTITYLIST_ROWS + " " + PSB_MATCOMP_ENTITYLIST_COLS, working_dir=op_dir)
    print("sys_call_result", sys_call_result)
    # op_dir += "/.."
    psb_matcomp_img = []
    if os.path.isfile(os.path.join(op_dir, PSB_MATCOMP_OUT_FILES[0])):
        psb_matcomp_img.append('{0}'.format(get_string_for_png(os.path.join(op_dir, PSB_MATCOMP_OUT_FILES[0]))))
    return psb_matcomp_img

# def compute_psb_f1score_for_factor(op_dir, fact_name):
#     # sys_call_result = make_system_call("bash " + PSB_F1SCORE_SCRIPT_PATH + " " + op_dir + " " + fact_name + " " + psb_f1score_ENTITYLIST_FILENAME, working_dir=op_dir)
#     # print("sys_call_result", sys_call_result)
#     op_dir += "/.."
#     psb_f1score_img = []
#     if os.path.isfile(os.path.join(op_dir, PSB_F1SCORE_OUT_FILES[0])):
#         psb_f1score_img.append('{0}'.format(get_string_for_png(os.path.join(op_dir, PSB_F1SCORE_OUT_FILES[0]))))
#     return psb_f1score_img

def compute_psb_pr_for_factor(op_dir, fact_name):
    sys_call_result = make_system_call("bash " + PSB_PR_SCRIPT_PATH + " " + op_dir + " " + fact_name + " " + PSB_PR_OUT_FILES[0], working_dir=op_dir)
    print("sys_call_result", sys_call_result)
    # op_dir += "/.."
    psb_pr_img = []
    if os.path.isfile(os.path.join(op_dir, PSB_PR_OUT_FILES[0])):
        psb_pr_img.append('{0}'.format(get_string_for_png(os.path.join(op_dir, PSB_PR_OUT_FILES[0]))))
    return psb_pr_img

def compute_psb_roc_for_factor(op_dir, fact_name):
    sys_call_result = make_system_call("bash " + PSB_ROC_SCRIPT_PATH + " " + op_dir + " " + fact_name + " " + PSB_ROC_OUT_FILES[0], working_dir=op_dir)
    print("sys_call_result", sys_call_result)
    # op_dir += "/.."
    psb_roc_img = []
    if os.path.isfile(os.path.join(op_dir, PSB_ROC_OUT_FILES[0])):
        psb_roc_img.append('{0}'.format(get_string_for_png(os.path.join(op_dir, PSB_ROC_OUT_FILES[0]))))
    return psb_roc_img

def compute_clusters_for_factor(op_dir, fact_name):
    sys_call_result = make_system_call("bash " + CLUSTERS_SCRIPT_PATH + " " + op_dir + " " + fact_name + " " + CLUSTERS_ENTITYLIST_FILENAME, working_dir=op_dir)
    print("sys_call_result", sys_call_result)
    clusters_img = []
    if os.path.isfile(os.path.join(op_dir, "clusters_from_factor.png")):
        clusters_img.append('{0}'.format(get_string_for_png(os.path.join(op_dir, "clusters_from_factor.png"))))
    return clusters_img
    
def compute_enrichments_for_clusters(op_dir, fact_name, enrichments_anno):
    sys_call_result = make_system_call("bash " + ENRICHMENTS_SCRIPT_PATH + " " + op_dir + " " + fact_name + " " + CLUSTERS_ENTITYLIST_FILENAME + " " + enrichments_anno, working_dir=op_dir)
    print("sys_call_result", sys_call_result)
    clusters_img = []
    if os.path.isfile(os.path.join(op_dir, "enrichments_for_clusters.png")):
        clusters_img.append('{0}'.format(get_string_for_png(os.path.join(op_dir, "enrichments_for_clusters.png"))))
    return clusters_img

def compute_icell_for_factor(op_dir, fact_name, genelist, output_filename):
    print("compute_icell_for_factor")
    sys_call_result = make_system_call("bash " + ICELL_SCRIPT_PATH + " " + genelist + " " + fact_name + " " + output_filename, working_dir=op_dir)
    print("sys_call_result", sys_call_result)

def compute_gdv_for_icell(op_dir, file_name):
    sys_call_result = make_system_call("bash " + GDV_SCRIPT_PATH + " " + op_dir + " " + file_name + " " , working_dir=op_dir)
    print("sys_call_result", sys_call_result)
    return sys_call_result

def compute_gdv_similarities(op_dir, genelist, gdv_filenames, output_filename):
    print("compute_gdv_similarities")
    sys_call_result = make_system_call("bash " + GDVSIM_SCRIPT_PATH + " " + ICELL_GDV_FILENAME + " " + genelist + " " + output_filename + " " + " ".join(gdv_filenames), working_dir=op_dir)
    print("sys_call_result", sys_call_result)
    return sys_call_result

def get_all_results(task):
    # from CanonicalAnalysis
    res_facts = []
    op_dir = COMPUTATIONS_DIR + "/" + task.operational_directory

    facts = pickle.load(open(op_dir + "/facts.pkl", "rb"))
    print("facts", facts)
    print("type(facts)", type(facts))
    print("type(facts[0])", type(facts[0]))
    print("facts[0].keys()", facts[0].keys())

    losses = np.load(os.path.join(op_dir, "losses.npy"))
    
    for f_id, fact in enumerate(facts):
        print("for fact:", fact)
        res_facts.append(DataFusionResult(title="Fact " + str(f_id), fact=fact))

    extra_res = []
    if os.path.isfile(os.path.join(op_dir, "clusters_example.png")):
        extra_res.append('{0}'.format(get_string_for_png(os.path.join(op_dir, "clusters_example.png"))))
    if os.path.isfile(os.path.join(op_dir, "enrichment_example.png")):
        extra_res.append('{0}'.format(get_string_for_png(os.path.join(op_dir, "enrichment_example.png"))))

    return res_facts, [output[0] for output in get_all_downloadable_results(task)], extra_res

def get_string_for_png(file_path):
    output = StringIO.StringIO()
    im = Image.open(file_path)
    im.save(output, format='PNG')
    output.seek(0)
    output_s = output.read()
    b64 = base64.b64encode(output_s)
    return '{0}'.format(b64)

def get_all_downloadable_results(task):
    results = []
    op_dir = COMPUTATIONS_DIR + "/" + task.operational_directory
    for r_file in RESULTS_FILES:
        if r_file.endswith("*"):
            pattern = r_file
            for path, _, files in os.walk(op_dir):
                for name in files:
                    if fnmatch(name, pattern):
                        results.append((name, open(os.path.join(path, name)).read()))
        else:
            file_path = COMPUTATIONS_DIR + "/" + task.operational_directory + "/" + r_file
            if os.path.isfile(file_path):
                results.append([r_file, open(file_path).read()])
    return results

class DataFusionResult:
    def __init__(self, title, fact):
        self.title = title
        self.fact = fact
        self.counter = fact["counter"]
        self.props = []
        for key in fact.keys():
            self.props.append((key, fact[key]))


    # def get_graph_image(self):
    #     return self.result_graph

    def get_properties(self):
        return self.props

    def get_title(self):
        return self.title

    def get_counter(self):
        return self.counter

    def get_output_files(self):
        return 

def __get_matrix_table_for_results(props):
    # from networkprops
    heading = ["Name", "Nodes", "Edges", "Clustering Coefficient", "Average Path Length", "Diameter"]
    rows = []
    gcm_raw_data = []
    network_names = []
    for prop in props:
        rows.append([
            prop.name,
            prop.number_of_nodes,
            prop.number_of_edges,
            prop.ccoeff,
            prop.avg_path_length,
            prop.diameter
        ])
        network_names.append(prop.name)
        gcm_raw_data.append([prop.name, prop.get_gcm_matrix_png_data()])
    return heading, rows, gcm_raw_data, network_names

class NetworkPropertiesResult:
    def __init__(self):
        self.ccoeff = 0
        self.avg_path_length = 0
        self.degree_dist = []
        self.name = ""
        self.id = None
        self.gcm_matrix_png_data = None
        self.error_while_gcm_matrix = False
        self.number_of_nodes = 0
        self.number_of_edges = 0
        self.diameter = 0

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_avg_path_length(self):
        return self.avg_path_length

    def get_degree_dist(self):
        return self.degree_dist

    def get_gcm_matrix_png_data(self):
        return str(self.gcm_matrix_png_data)

    def did_error_occur_while_gcm_computation(self):
        return self.error_while_gcm_matrix

    def get_ccoeff(self):
        return self.ccoeff

    def __str__(self):
        return "ccoeff: " + str(self.ccoeff) + ", Avg PL: " + str(self.avg_path_length) + ", Deg Dist: " + str(
            self.degree_dist)

def get_df_result_for_task(task):
    # from networkalignment
    return open(COMPUTATIONS_DIR + "/" + task.operational_directory + "/" + RESULT_VIEW_FILE).read()

"""
class DfResult():
    alignment = ""
    error = ""
    properties = []
    graph1_name = ""
    graph2_name = ""
    task = ""

    def __init__(self, properties=[], alignment=[], network_1_name=None, network_2_name=None, operational_dir=""):
        self.properties = properties
        self.alignment = alignment
        self.network_1_name = network_1_name
        self.network_2_name = network_2_name
        self.operational_dir = operational_dir

    def __format_alignment_string(self):
        result = []
        if isinstance(self.alignment, str):
            for pair in self.alignment.split("\n"):
                if pair:
                    nodes = pair.split()
                    if len(nodes) == 2:
                        result.append((nodes[0], nodes[1]))
        self.alignment = result

    def has_properties(self):
        return len(self.properties) != 0

    def error_occurred(self):
        return self.error != ""

    def get_error_text(self):
        return self.error

    def get_network_1_name(self):
        return self.graph1_name

    def get_network_2_name(self):
        return self.graph2_name

    def get_properties(self):
        return self.properties

    def get_alignment(self):
        return self.alignment

    def save_results(self):
        f = open(self.operational_dir + "/" + RESULT_VIEW_FILE, "w")
        self.__format_alignment_string()
        context = Context({'result': self})
        f.write(get_template("NetworkAlignment/alignment_result.html").render(context))
        f.close()

    def __str__(self):
        return "Alignment: " + str(self.alignment) + "Properties: " + str(self.properties)
"""