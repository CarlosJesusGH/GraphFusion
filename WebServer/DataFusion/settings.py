__author__ = 'carlos garcia-hernandez'  # using as reference: WebServer/CanonicalCorrelationAnalysis/settings.py and WebServer/NetworkAlignment/settings.py

import os

DATA_FUSION_TASK = "DataFusion"
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
__EXECUTABLE_PATH = FILE_DIR + "/executable"
__SCRIPTS_PATH = FILE_DIR + "/scripts/"
# NCOUNT_PATH = __EXECUTABLE_PATH + "/ncount"
# ORCA_PATH = __EXECUTABLE_PATH + "/orca"
COMPUTATIONS_DIR = FILE_DIR + "/computations"
# script_paths
DATA_FUSION_SCRIPT_PATH = __SCRIPTS_PATH + "DataFusionScript.py"
TEST_SCRIPT_PATH = __SCRIPTS_PATH + "test_script.py"
PYNMF_SCRIPT_PATH = __SCRIPTS_PATH + "include/pynmf/pynmf_shell_script.sh"
CLUSTERS_SCRIPT_PATH = __SCRIPTS_PATH + "include/clusters/clusters_shell_script.sh"
ENRICHMENTS_SCRIPT_PATH = __SCRIPTS_PATH + "include/enrichments/enrichments_shell_script.sh"
ICELL_SCRIPT_PATH = __SCRIPTS_PATH + "include/icell/icell_shell_script.sh"
GDV_SCRIPT_PATH = __SCRIPTS_PATH + "include/gdv/gdv_shell_script.sh"
GDVSIM_SCRIPT_PATH = __SCRIPTS_PATH + "include/gdvsim/pan_gdvsim_shell_script.sh"
PSB_ROC_SCRIPT_PATH = __SCRIPTS_PATH + "include/psb/psb_roc_shell_script.sh"
PSB_ROC_OUT_FILES = ["psb_roc_curve.png"]
PSB_PR_SCRIPT_PATH = __SCRIPTS_PATH + "include/psb/psb_pr_shell_script.sh"
PSB_PR_OUT_FILES = ["psb_pr_curve.png"]
PSB_F1SCORE_SCRIPT_PATH = __SCRIPTS_PATH + "include/psb/psb_f1score_shell_script.sh"
PSB_F1SCORE_OUT_FILES = ["psb_f1score_computation.png"]
PSB_MATCOMP_SCRIPT_PATH = __SCRIPTS_PATH + "include/psb/psb_matcomp_shell_script.sh"
PSB_MATCOMP_OUT_FILES = ["psb_matcomp_distribution.png", "psb_matcomp_predictions.csv"]
PSB_MATCOMP_ENTITYLIST_ROWS = "psb_matcomp_entitylist_rows.csv"
PSB_MATCOMP_ENTITYLIST_COLS = "psb_matcomp_entitylist_cols.csv"
# others
RESULT_VIEW_FILE = "result.html"
NAMES_MAPPING_FILE = "names.mapping"
NAMES_OF_NETWORKS_LIST_FILES = ["list_1.txt", "list_2.txt"]
CLUSTERS_ENTITYLIST_FILENAME = "clusters_entitylist.csv"
ENRICHMENTS_ANNO_FILENAME = "enrichments_annotations.csv"
ICELL_FILENAME = "iCell.edgelist"
ICELL_GENELIST_FILENAME = "icell_genelist.csv"
ICELL_GDV_FILENAME = "iCell.ndump2"
GDV_SIMS_COMP_FOLDER = "gdv_sims"
GDV_SIMS_FILENAME = "iCell_rewired.csv"
GDV_GENELIST_FILENAME = "genelist.csv"
RESULTS_FILES = [   "losses.npy",
                    "facts.pkl",
                    "fact_S_*",
                    "fact_G_*",
                    "fact_F_*",
                    ICELL_FILENAME,]

FACTORIZATION_TYPE = [  
    ("", "Type of factorization"),
    ("NMF", "NMF Factorization"),
    ("NMTF", "NMTF Factorization"), 
    ("SNMF", "SNMF Factorization"), 
    ("SNMTF", "SNMTF Factorization")]
    
FACTOR_INIT_TYPE = [
    # ("", "Type of initialization"),
    # ("load", "Load from matrices"), 
    ("random", "Random initialization"),
    ("tsvd", "SVD initialization"),
    ]

FACTOR_SHARE_DIRECTION = [
    ("", "Factor sharing"),
    ("up", "Share factor upwards"), 
    ("down", "Share factor downwards"),
    ("updown", "Share factor upwards+downwards")]