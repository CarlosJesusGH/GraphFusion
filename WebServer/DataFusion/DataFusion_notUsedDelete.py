__author__ = 'carlos garcia-hernandez'
# reference: WebServer/NetworkProperties/NetworkProperties.py

# from NetworkAlignment.ORCAThreadRunner import ORCAExecutable
# from WebServer.DataFusion.scripts.include.pynmf.PyNmf import PyNmf
# from utils.SystemCall import make_system_call
# from .settings import COMPUTE_GCM_PATH
# from NetworkAlignment.GraphFileConverter import ListToLeda
# from WebServer.settings_common import PYTHON_PATH
# import networkx as nx
# from PIL import Image
# import base64
# import StringIO
import logging

# from WebServer.DataFusion.scripts.include.pynmf.PyNmf import *
# from .PyNmf2 import *
# from .include.pynmf.PyNmf import *
# from .scripts.include.pynmf.PyNmf3 import *
# from WebServer.DataFusion.scripts.include.pynmf.PyNmf3 import *
# import os
# ######
# from .scripts.include.pynmf.PyNmf import *
# from scripts.include.pynmf.PyNmf import *

LOGGER = logging.getLogger(__name__)

""""
class Graph():
    def __init__(self):
        self.graph = None
        self.content = None

    def parse_content(self, content):
        if isinstance(content, str):
            content = content.split("\n")
        self.content = content
        if content[0].startswith("LEDA.GRAPH"):
            self.parse_graph_leda(content)
        else:
            self.parse_graph_edge_list(content)

    def parse_graph_edge_list(self, content):
        self.graph = nx.parse_edgelist(content)

    def parse_graph_leda_file(self, path):
        self.graph = nx.read_leda(path)

    def parse_graph_leda(self, content):
        self.graph = nx.parse_leda(content)

    def parse_graph_edge_list_file(self, path):
        self.graph = nx.read_edgelist(path)

    def nodes(self):
        return nx.nodes(self.graph)

    def edges(self):
        return self.graph.edges()

    def degrees(self):
        return self.graph.degree()

def get_string_for_png(file_path):
    output = StringIO.StringIO()
    im = Image.open(file_path)
    im.save(output, format='PNG')
    output.seek(0)
    output_s = output.read()
    b64 = base64.b64encode(output_s)
    return '{0}'.format(b64)
"""

class DataFusion: #(Graph):
    def __init__(self, operational_dir, facts):
        self.result = DataFusionResult()
        self.operational_dir = operational_dir
        self.facts = facts
        self.graph_path = self.operational_dir + "/" + self.graph_name

    def perform_datafusion(self):
        self.result.ccoeff = 0
        num_connected_comps = 0
        self.result.avg_path_length = 0
        self.result.diameter = 0
        self.result.degree_dist = 0
        self.result.number_of_edges = 0
        self.result.number_of_nodes = 0
        # nmf = PyNmf(self.operational_dir, self.facts)
        # nmf.run_nmf()


class DataFusionResult:
    def __init__(self):
        self.ccoeff = 0
        self.avg_path_length = 0
        self.degree_dist = []
        self.name = ""
        self.id = None
        self.gcm_matrix_png_data = None
        self.error_while_gcm_matrix = False
        self.number_of_nodes = 0
        self.number_of_edges = 0
        self.diameter = 0

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_avg_path_length(self):
        return self.avg_path_length

    def get_degree_dist(self):
        return self.degree_dist

    def get_gcm_matrix_png_data(self):
        return str(self.gcm_matrix_png_data)

    def did_error_occur_while_gcm_computation(self):
        return self.error_while_gcm_matrix

    def get_ccoeff(self):
        return self.ccoeff

    def __str__(self):
        return "ccoeff: " + str(self.ccoeff) + ", Avg PL: " + str(self.avg_path_length) + ", Deg Dist: " + str(
            self.degree_dist)
