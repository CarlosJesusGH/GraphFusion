__author__ = 'carlos garcia-hernandez' 

import os

PROBABILISTIC_NETWORKS_NET_ANALYSIS_TASK = "ProbabilisticNetworksNetAnalysisTask"
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
__SCRIPTS_PATH = FILE_DIR + "/scripts/"
COMPUTATIONS_DIR = FILE_DIR + "/computations"
# script_paths
BASH_SCRIPT_PATH = __SCRIPTS_PATH + "bash_script.sh"
PYTHON_SCRIPT_PATH = __SCRIPTS_PATH + "pyhon_script.sh"
PROBABILISTIC_NETWORKS_NET_ANALYSIS_SCRIPT_IN_FILES = ["input_file1.tmp", "input_file2.tmp"]
PROBABILISTIC_NETWORKS_NET_ANALYSIS_SCRIPT_OUT_FILES = ["output_file1.tmp", "output_file2.tmp"]
# others
RESULT_VIEW_FILE = "result.html"
RESULT_FILES = ["results.txt", 
                "Gene_Names_*", 
                "Work_Network_Bin_*", 
                "Work_Network_Prob_*", 
                "GDV_Work_Network_Bin_*", 
                "GDV_Work_Network_Prob_*"
                ]
REQUEST_FILES = []
# for network properties
COMPUTE_GCM_PATH = FILE_DIR + "/scripts/ComputeGCM.py"
DEGREE_DISTRIBUTION_FILE = "Degree_Dist.png"
NAMES_MAPPINGS_FILE = "mappings.txt"
# options for selectors
METHOD_TYPE = [  
    ("", "Type of method"),
    ("TYPE1", "TYPE1 method"),
    ("TYPE2", "TYPE2 method"), 
    ("TYPE3", "TYPE3 method")]
    