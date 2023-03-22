__author__ = 'varun'

from .AbstractGraphModelGenerator import AbstractGraphModelGenerator
import networkx as nx


class SFGraphModelGenerator(AbstractGraphModelGenerator):
    def __init__(self, number_of_nodes, number_of_edges):
        AbstractGraphModelGenerator.__init__(self, number_of_edges=number_of_edges, number_of_nodes=number_of_nodes)

    def get_graph(self):
        m = self.number_of_edges / self.number_of_nodes
        return nx.barabasi_albert_graph(self.number_of_nodes, m + 1)