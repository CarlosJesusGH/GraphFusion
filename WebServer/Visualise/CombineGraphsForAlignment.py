__author__ = 'varun'

import networkx as nx
import logging

LOGGER = logging.getLogger(__name__)


class AlignmentGraph:
    def __init__(self, graph1, graph2, alignment):
        self.graph1 = graph1.graph
        self.graph2 = graph2.graph
        self.alignment = self.__change_alignment_to_dict(alignment=alignment)

    def __change_alignment_to_dict(self, alignment):
        mapping = {}
        for line in alignment.split("\n"):
            linesplit = line.strip().split()
            if len(linesplit) > 1:
                prot1 = linesplit[0]
                prot2 = linesplit[1]
                if self.graph1.has_node(prot1) and self.graph2.has_node(prot2):
                    mapping[prot1] = prot2
                elif self.graph1.has_node(prot2) and self.graph2.has_node(prot1):
                    mapping[prot2] = prot1
        return mapping

    def get_aligned_graph(self):
        ali_1 = []
        ali_2 = []
        for key in self.alignment.keys():
            ali_1.append(key)
            ali_2.append(self.alignment[key])

        common_graph = nx.Graph()
        for i in range(len(ali_1)):
            row1 = ali_1[i]
            col1 = ali_2[i]
            for j in range(i + 1, len(ali_1)):
                row2 = ali_1[j]
                col2 = ali_2[j]
                if self.graph1.has_edge(row1, row2) and self.graph2.has_edge(col1, col2):
                    common_graph.add_edge(row1 + "_" + col1, row2 + "_" + col2)
        return common_graph