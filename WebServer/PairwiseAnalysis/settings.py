__author__ = 'varun'

import os

PAIRWISE_ANALYSIS_TASK = "PairwiseAnalysis"
PAIRWISE_ANALYSIS_COMPUTATIONS_DIR = os.path.dirname(os.path.abspath(__file__)) + "/computations"
NETWORK_COMPARISON_SCRIPT = os.path.dirname(os.path.abspath(__file__)) + "/NetworkComparison.py"
# ('rgf', 'RGF distance') uses second part for viewing in UI to user, and the 'rgf' part is the analysis
# type from the NetworkComparison.py script
DISTANCES = [
    ('rgf', "RGF distance"),
    ('gdda', "GDD Agreement"),
    ('degree', "Degree distribution"),
    ('clustering', "Clustering Coefficient"),
    ('diameter', "Diameter"),
    ('spectral', "Spectral distance using the eigenvalues of the Laplacian representation"),
    ('gcd11', "Graphlet Correlation distance with non-redundant 2-to-4 node graphlet orbits"),
    ('gcd15', "Graphlet Correlation distance with all 2-to-4 node graphlet orbits"),
    ('gcd73', "Graphlet Correlation distance with all 2-to-5 node graphlet orbits"),
    ('gcd58', "Graphlet Correlation distance with non-redundant 2-to-5 node graphlet orbits")]
RESULT_FILES = {
    'rgf.txt': "RGF distance",
    'gdda.txt': "GDD Agreement Arithmetic",
    'gddg.txt': "GDD Agreement Geometric",
    'degree_dists.txt': "Degree distribution",
    'clust_coef.txt': "Clustering Coefficient",
    'gcd58.txt': "Graphlet Correlation distance with non-redundant 2-to-5 node graphlet orbits",
    'gcd73.txt': "Graphlet Correlation distance with all 2-to-5 node graphlet orbits",
    'diameter.txt': "Diameter",
    'gcd11.txt': "Graphlet Correlation distance with non-redundant 2-to-4 node graphlet orbits",
    'gcd15.txt': "Graphlet Correlation distance with all 2-to-4 node graphlet orbits",
    'spectralDist.txt': "Spectral distance using the eigenvalues of the Laplacian representation"
}
NAMES_MAPPING_FILE = "names_to_file_mapping.txt"
NAMES_OF_NETWORKS_LIST_FILES = ["list_1.txt", "list_2.txt"]