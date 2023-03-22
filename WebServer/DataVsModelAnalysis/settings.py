__author__ = 'varun'

import os
from collections import OrderedDict

MODELS_INFO_FILE = "models_info.txt"
DATA_VS_MODEL_TASK = "DataVsModel"
DATA_VS_MODEL_COMPUTATIONS_DIR = os.path.dirname(os.path.abspath(__file__)) + "/computations"
GEOMETRIC_MODEL_BIN_COUNT = 10
# MODELS = {
#     "ER": "Erdos-Renyi",
#     # "ERDD": "Erdos-Renyi with Degree Distribution",
#     "GEO": "Geometric",
#     "GEOGD": "Geometric with Gene Duplication",
#     "SF": "Scale Free",
#     "SFGD": "Scale Free with Gene Duplication",
#     "Sticky": "Sticky Preferential Attachment"
# }
MODELS = OrderedDict([
    ('ER', 'Erdos-Renyi'),
    ('GEO', 'Geometric'),
    ('GEOGD', 'Geometric with Gene Duplication'),
    ('SF', 'Scale Free'),
    ('SFGD', 'Scale Free with Gene Duplication'),
    ('Sticky', 'Sticky Preferential Attachment'),
])

RESULT_IMAGE_FILES = {
    'rgf.png': "RGF distance",
    'gdda.png': "GDD Agreement Arithmetic",
    'gddg.png': "GDD Agreement Geometric",
    'degree_dists.png': "Degree distribution",
    'clust_coef.png': "Clustering Coefficient",
    'gcd58.png': "Graphlet Correlation distance with non-redundant 2-to-5 node graphlet orbits",
    'gcd73.png': "Graphlet Correlation distance with all 2-to-5 node graphlet orbits",
    'diameter.png': "Diameter",
    'gcd11.png': "Graphlet Correlation distance with non-redundant 2-to-4 node graphlet orbits",
    'gcd15.png': "Graphlet Correlation distance with all 2-to-4 node graphlet orbits",
    'spectralDist.png': "Spectral distance using the eigenvalues of the Laplacian representation of the network"
}