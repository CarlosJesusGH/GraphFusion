__author__ = 'varun'

import os

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
__EXECUTABLE_PATH = FILE_DIR + "/executable"
GRAAL_PATH = __EXECUTABLE_PATH + "/GRAAL"
MI_GRAAL_PATH = __EXECUTABLE_PATH + "/MI-GRAAL"
L_GRAAL_PATH = __EXECUTABLE_PATH + "/L-GRAAL"
C_GRAAL_PATH = __EXECUTABLE_PATH + "/CGRAAL"
NCOUNT_PATH = __EXECUTABLE_PATH + "/ncount"
ORCA_PATH = __EXECUTABLE_PATH + "/orca"
COMPUTATIONS_DIR = FILE_DIR + "/computations"
ALIGNMENT_TASK = "Alignment"
RESULT_VIEW_FILE = "result.html"
NAMES_MAPPING_FILE = "names.mapping"

RESULTS_FILES = ["result.aln", "result.ealn", "result.nealn", "result.results"]