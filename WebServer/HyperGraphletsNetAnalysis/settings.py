__author__ = 'carlos garcia-hernandez' 

import os

HYPERGRAPHLETS_NET_ANALYSIS_TASK = "HyperGraphletsNetAnalysisTask"
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
__SCRIPTS_PATH = FILE_DIR + "/scripts/"
COMPUTATIONS_DIR = FILE_DIR + "/computations"
# script_paths
BASH_SCRIPT_PATH = __SCRIPTS_PATH + "bash_script.sh"
PYTHON_SCRIPT_PATH = __SCRIPTS_PATH + "pyhon_script.sh"
HDV_SIGNATURES_SCRIPT = __SCRIPTS_PATH + "hypergraphlet_counter/source/run_hypercounter"
HYPERGRAPHLETS_NET_ANALYSIS_SCRIPT_IN_FILES = ["input_file1.tmp", "input_file2.tmp"]
HYPERGRAPHLETS_NET_ANALYSIS_SCRIPT_OUT_FILES = ["output_file1.tmp", "output_file2.tmp"]
# others
RESULT_VIEW_FILE = "result.html"
RESULT_FILES = ["output.hdv", 
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
    