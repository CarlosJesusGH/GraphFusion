__author__ = 'varun'

from NetworkAlignment.ORCAThreadRunner import ORCAExecutable
from utils.SystemCall import make_system_call
from .settings import DN_COMPUTE_GCM_PATH
from NetworkAlignment.GraphFileConverter import ListToLeda
from WebServer.settings_common import PYTHON_PATH
import networkx as nx
from PIL import Image
import base64
import StringIO
import logging
import os

LOGGER = logging.getLogger(__name__)


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


class DirectedNetworkProperties(Graph):
    def __init__(self, graph_name, operational_dir):
        Graph.__init__(self)
        self.result = NetworkPropertiesResult()
        self.operational_dir = operational_dir
        self.graph_name = graph_name
        self.graph_path = self.operational_dir + "/" + self.graph_name

    def evaluate_heat_map_for_gcm(self):
        f = open(self.graph_path, "w")
        if self.content[0].startswith("LEDA.GRAPH"):
            f.write("\n".join(self.content))
        else:
            f.write(ListToLeda(graph_list="\n".join(self.content)).convert_to_leda())
        f.close()
        self.result.gdd_signatures = ORCAExecutable(self.graph_path).run()
        ndump_file = self.operational_dir + "/" + self.graph_name + ".res.ndump2"
        if os.path.isfile(ndump_file):
            command = PYTHON_PATH + " " + DN_COMPUTE_GCM_PATH + " " + self.graph_name + ".res.ndump2 73 0"
            LOGGER.info("Making system call: " + command)
            sys_result = make_system_call(command, working_dir=self.operational_dir)
            LOGGER.info(sys_result.stdout)
            LOGGER.error(sys_result.stderr)
            if os.path.isfile(self.operational_dir + "/" + self.graph_name + ".res_gcm73.png"):
                self.result.gcm_matrix_png_data = '{0}'.format(
                    get_string_for_png(self.operational_dir + "/" + self.graph_name + ".res_gcm73.png"))
                LOGGER.info("PNG Data: " + str(len(self.result.gcm_matrix_png_data)))
            else:
                self.result.error_while_gcm_matrix = True
        else:
            self.result.error_while_gcm_matrix = True

    @classmethod
    def __get_avg_path_length(cls, graph):
        if len(nx.nodes(graph)) == 1:
            return 0
        else:
            return nx.average_shortest_path_length(graph)

    def evaluate_properties(self):
        self.result.ccoeff = nx.average_clustering(self.graph)
        if nx.is_connected(self.graph):
            self.result.avg_path_length = nx.average_shortest_path_length(self.graph)
            self.result.diameter = nx.diameter(self.graph)
        else:
            num_connected_comps = 0
            self.result.avg_path_length = 0
            self.result.diameter = 0
            for comp in nx.connected_component_subgraphs(self.graph):
                self.result.avg_path_length += self.__get_avg_path_length(comp)
                self.result.diameter += nx.diameter(comp)
                if nx.number_of_nodes(comp) != 1:
                    num_connected_comps += 1
            self.result.avg_path_length /= num_connected_comps
        self.result.degree_dist = sorted(nx.degree(self.graph).values(), reverse=True)
        self.result.number_of_edges = len(self.edges())
        self.result.number_of_nodes = len(self.nodes())
        self.evaluate_heat_map_for_gcm()


class NetworkPropertiesResult:
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
