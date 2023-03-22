__author__ = 'varun'

import os

CANONICAL_CORRELATION_TASK = "CanonicalCorrelation"
CANONICAL_CORRELATION_COMPUTATIONS_DIR = os.path.dirname(os.path.abspath(__file__)) + "/computations"
NAMES_MAPPING_FILE_NAME = "names.mappings"
__SCRIPTS_PATH = os.path.dirname(os.path.abspath(__file__)) + "/scripts/"
ANNOTATIONS_RETRIEVER_SCRIPT_PATH = __SCRIPTS_PATH + "Generate_GO.py"
MAKE_GO_MATRIX_SCRIPT_PATH = __SCRIPTS_PATH + "Make_GO_Matrix.py"
CCA_GENERATION_SCRIPT_PATH = __SCRIPTS_PATH + "CCA_Step1_R.py"
GENERATE_PLOT_SCRIPT_PATH = __SCRIPTS_PATH + "Autoplot_CCA.py"
CCA_R_SCRIPT = __SCRIPTS_PATH + "my_CCA.R"
GENE_TO_GO_FILE = __SCRIPTS_PATH + "gene2go"
OBO_FILE = __SCRIPTS_PATH + "go-basic.obo"
PLOT_FILE_KEEP_VARIABLE = "5"

ANNOTATIONS_TYPE = [("MF", "Molecular Function"), ("BP", "Biological Process"), ("CC", "Cellular Component")]

# results files
ANNOTATIONS_FILENAME = "annotations.txt"
GO_MATRIX_FILE_NAME = "annotations_matrix.txt"
CCA_RESULT_FILENAME = "cca_result"
CCA_RESULT_FIGURE_PREFIX = "cca_result_cancor_"