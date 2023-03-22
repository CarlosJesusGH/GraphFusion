__author__ = 'varun'

import networkx as nx
import numpy as np
from .AbstractDiGraphModelGenerator import AbstractDiGraphModelGenerator


class DiERGraphModelModelGenerator(AbstractDiGraphModelGenerator):
    def __init__(self, number_of_nodes, number_of_edges):
        AbstractDiGraphModelGenerator.__init__(self, number_of_edges=number_of_edges, number_of_nodes=number_of_nodes)

    def get_graph(self):
        # from header note in: WebServer/DirectedNetworkDataVsModel/scripts/reference_generate_DiRandomGraphs_dif_dens.py
        # p = self.number_of_edges / self.number_of_nodes
        p = 0.005
        # print("*** self.number_of_nodes self.number_of_edges, p", self.number_of_nodes self.number_of_edges, p)
        return nx.erdos_renyi_graph(self.number_of_nodes,p,directed=True)
    