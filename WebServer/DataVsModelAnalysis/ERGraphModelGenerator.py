__author__ = 'varun'

import networkx as nx
import numpy as np
from .AbstractGraphModelGenerator import AbstractGraphModelGenerator


class ERGraphModelModelGenerator(AbstractGraphModelGenerator):
    def __init__(self, number_of_nodes, number_of_edges):
        AbstractGraphModelGenerator.__init__(self, number_of_edges=number_of_edges, number_of_nodes=number_of_nodes)

    def get_graph(self):
        total_edge = (self.number_of_nodes * (self.number_of_nodes - 1)) / 2
        pos_edges = {}
        k = 0
        for i in range(self.number_of_nodes):
            for j in range(i + 1, self.number_of_nodes):
                pos_edges[k] = [i, j]
                k += 1

        # random edge sampling without replacment
        rand_edges = np.random.permutation(np.arange(total_edge))[:self.number_of_edges]

        graph = nx.Graph()
        graph.add_nodes_from(range(self.number_of_edges))

        for k in rand_edges:
            graph.add_edge(pos_edges[k][0], pos_edges[k][1])

        return graph