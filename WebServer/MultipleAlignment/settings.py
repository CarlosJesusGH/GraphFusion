__author__ = 'carlos garcia-hernandez'  # using as reference: WebServer/CanonicalCorrelationAnalysis/settings.py and WebServer/NetworkAlignment/settings.py

import os

MULTIPLE_ALIGNMENT_TASK = "MultipleAlignmentTask"
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
__SCRIPTS_PATH = FILE_DIR + "/scripts/"
COMPUTATIONS_DIR = FILE_DIR + "/computations"
# script_paths
BASH_SCRIPT_PATH = __SCRIPTS_PATH + "bash_script.sh"
PYTHON_SCRIPT_PATH = __SCRIPTS_PATH + "pyhon_script.sh"
TEMPLATE_SCRIPT_IN_FILES = ["input_file1.tmp", "input_file2.tmp"]
TEMPLATE_SCRIPT_OUT_FILES = ["output_file1.tmp", "output_file2.tmp"]
# others
RESULT_VIEW_FILE = "result.html"
NAMES_MAPPING_FILE = "names.mapping"
RESULT_FILES = [   "fuse_alignment_output.txt",
                    "nmtf_scores.lst",
                    "network_list.txt",]
REQUEST_FILES = ["sequence_scores.lst",]
# options for selectors
METHOD_TYPE = [  
    ("", "Type of method"),
    ("TYPE1", "TYPE1 method"),
    ("TYPE2", "TYPE2 method"), 
    ("TYPE3", "TYPE3 method")]
    