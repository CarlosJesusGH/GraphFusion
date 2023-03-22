__author__ = 'varun'

from .AbstractGraphModelGenerator import AbstractGraphModelGenerator
import networkx as nx
import random as rd
import math


class StickyGraphModelGenerator(AbstractGraphModelGenerator):
    def __init__(self, nodes, degrees):
        AbstractGraphModelGenerator.__init__(self, number_of_nodes=len(nodes), number_of_edges=-1)
        self.degrees = degrees
        self.nodes = nodes

    def get_graph(self):
        sum_degree = 0
        for node in self.nodes:
            sum_degree += self.degrees[node]

        sticky_index = {}
        for node in self.nodes:
            si = float(self.degrees[node]) / math.sqrt(float(sum_degree))
            sticky_index[node] = si

        # Create Sticky Network
        Sticky = nx.Graph()
        Sticky.add_nodes_from(self.nodes)

        for i in range(self.number_of_nodes):
            n1 = self.nodes[i]
            s1 = sticky_index[n1]
            for j in range(i + 1, self.number_of_nodes):
                n2 = self.nodes[j]
                s2 = sticky_index[n2]
                r = rd.random()
                if r <= s1 * s2:
                    Sticky.add_edge(n1, n2)
        return Sticky

