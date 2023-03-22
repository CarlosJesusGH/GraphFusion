__author__ = 'carlos garcia-hernandez'

import os

DIRECTED_NETWORK_PAIRWISE_TASK = "DN_Pairwise"
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
PAIRWISE_ANALYSIS_COMPUTATIONS_DIR = FILE_DIR + "/computations"
__SCRIPTS_PATH = FILE_DIR + "/scripts/"
DGDV_SIGNATURES_SCRIPT = __SCRIPTS_PATH + "Directed_Graphlet_Counter_v3"
DN_COMPARISON_SCRIPT = __SCRIPTS_PATH + "dn_pairwise_comp_shell_script.sh"

# ('rgf', 'RGF distance') uses second part for viewing in UI to user, and the 'rgf' part is the analysis
# type from the NetworkComparison.py script
DISTANCES = [
    ('1', 'DGCD-13 distance using 2- to 3- node'),
    ('2', 'DGCD-129 distance using 2- to 4- node'),
    ('3', 'RDGF distance'),
    ('4', 'DGDDA'),
    ('5', 'Directed spectral distance'),
    ('6', 'In- and Out-degree distribution distances')]
RESULT_FILES = {
    'DGCD-13.txt': "DGCD-13",
    'DGCD-129.txt': "DGCD-129",
    "RDGF.txt": "RDGF",
    "gdda.txt": "GDDA",
    "gddg.txt": "GDDG",
    "Spectralv2.txt": "Spectral",
    "INDD.txt": "In-degree distribution distances",
    "OUTDD.txt": "Out-degree distribution distances",
}
NAMES_MAPPING_FILE = "names_to_file_mapping.txt"
NAMES_OF_NETWORKS_LIST_FILES = ["list_1.txt", "list_2.txt"]