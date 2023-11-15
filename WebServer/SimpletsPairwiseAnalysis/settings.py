__author__ = 'carlos garcia-hernandez' 

import os
from collections import OrderedDict

SIMPLETS_PAIRWISE_ANALYSIS_TASK = "SimpletsPairwiseAnalysisTask"
SIMPLETS_DVM_ANALYSIS_TASK = "SimpletsDvmAnalysisTask"
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
__SCRIPTS_PATH = FILE_DIR + "/scripts/"
COMPUTATIONS_DIR = FILE_DIR + "/computations"
# script_paths
BASH_SCRIPT_PATH = __SCRIPTS_PATH + "bash_script.sh"
PYTHON_SCRIPT_PATH = __SCRIPTS_PATH + "pyhon_script.sh"
SDV_SIGNATURES_SCRIPT = __SCRIPTS_PATH + "SCounter.exe"
SIMPLETS_COMPARISON_SCRIPT = __SCRIPTS_PATH + "simplets_pairwise_comp_shell_script.sh"
SIMPLETS_PAIRWISE_ANALYSIS_SCRIPT_IN_FILES = ["input_file1.tmp", "input_file2.tmp"]
SIMPLETS_PAIRWISE_ANALYSIS_SCRIPT_OUT_FILES = ["output_file1.tmp", "output_file2.tmp"]
# others
RESULT_VIEW_FILE = "result.html"
REQUEST_FILES = []
# for network properties
COMPUTE_GCM_PATH = FILE_DIR + "/scripts/ComputeGCM.py"
DEGREE_DISTRIBUTION_FILE = "Degree_Dist.svg"
NAMES_MAPPINGS_FILE = "mappings.txt"
# options for selectors
METHOD_TYPE = [  
    ("", "Type of method"),
    ("TYPE1", "TYPE1 method"),
    ("TYPE2", "TYPE2 method"), 
    ("TYPE3", "TYPE3 method")]
DISTANCES = [
    ('1', 'FDD (Facet Distribution Distance)'),
    ('2', 'SCD (Simplet Correlation Distance)')]
NAMES_OF_NETWORKS_LIST_FILES = ["list_1.txt", "list_2.txt"]
RESULT_FILES = {
    'FDD.txt': "FDD (Facet Distribution Distance)",
    'SCD.txt': "SCD (Simplet Correlation Distance)",
    }
RESULT_IMAGE_FILES = {
    'FDD.svg': "FDD (Facet Distribution Distance)",
    'SCD.svg': "SCD (Simplet Correlation Distance)",
}
# MODELS = {
#     "RCC": "random clique complex",
#     "VRC": "Vietoris-Rips complex",
#     "SFC": "scale-free complex",
#     "WSC": "Watts-Strogatz complex",
#     "LM-RCC": "Linial-Meshulam RCC",
#     "LM-VRC": "Linial-Meshulam VRC",
#     "LM-SFC": "Linial-Meshulam SFC",
#     "LM-WSC": "Linial-Meshulam WSC",
# }
MODELS = OrderedDict([
    ("RCC", "random clique complex"),
    ("VRC", "Vietoris-Rips complex"),
    ("SFC", "scale-free complex"),
    ("WSC", "Watts-Strogatz complex"),
    ("LM-RCC", "Linial-Meshulam RCC"),
    ("LM-VRC", "Linial-Meshulam VRC"),
    ("LM-SFC", "Linial-Meshulam SFC"),
    ("LM-WSC", "Linial-Meshulam WSC"),
])
NAMES_MAPPING_FILE = "names_to_file_mapping.txt"
    