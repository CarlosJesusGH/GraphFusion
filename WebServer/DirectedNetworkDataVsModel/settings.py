__author__ = 'varun'

import os
from collections import OrderedDict

MODELS_INFO_FILE = "models_info.txt"
DIRECTED_NETWORK_DVM_TASK = "DN_DataVsModel"
DATA_VS_MODEL_COMPUTATIONS_DIR = os.path.dirname(os.path.abspath(__file__)) + "/computations"
GEOMETRIC_MODEL_BIN_COUNT = 10
# MODELS = {
#     "DiER": "Di Erdos-Renyi",
#     # # "DiERDD": "Directed Erdos-Renyi with Degree Distribution",
#     "DiGEO": "Di Geometric",
#     "DiGEOGD": "Di Geometric with Gene Duplication",
#     "DiSF": "Di Scale Free",
#     "DiSFGD": "Di Scale Free with Gene Duplication",
#     # "DiSticky": "Di Sticky Preferential Attachment"
# }
MODELS = OrderedDict([
    ('DiER', 'Di Erdos-Renyi'),
    ('DiGEO', 'Di Geometric'),
    ('DiGEOGD', 'Di Geometric with Gene Duplication'),
    ('DiSF', 'Di Scale Free'),
    ('DiSFGD', 'Di Scale Free with Gene Duplication'),
])

RESULT_IMAGE_FILES = {
    'DGCD-13.svg': "DGCD-13",
    'DGCD-129.svg': "DGCD-129",
    "RDGF.svg": "RDGF",
    "gdda.svg": "GDDA",
    "gddg.svg": "GDDG",
    "Spectralv2.svg": "Spectral",
    "INDD.svg": "In-degree distribution distances",
    "OUTDD.svg": "Out-degree distribution distances",
}