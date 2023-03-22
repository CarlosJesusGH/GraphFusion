__author__ = 'varun'

from .AbstractGraphModelGenerator import AbstractGraphModelGenerator
from math import sqrt
from math import floor
import networkx as nx
import random


class GeometricGraphModelGenerator(AbstractGraphModelGenerator):
    def __init__(self, number_of_nodes, number_of_edges, bin_count):
        AbstractGraphModelGenerator.__init__(self, number_of_edges=number_of_edges, number_of_nodes=number_of_nodes)
        self.bin_count = bin_count

    @classmethod
    def __identifyCandidates(cls, node, binContents, neighborCount, binPerCoord):
        returnSet = set()

        for i in range(3):
            index = int(floor(node[i] * binPerCoord))

            candidateNodes = []
            for j in range(index - neighborCount, index + neighborCount + 1):
                try:
                    toPut = binContents[i][j]
                    candidateNodes.extend(toPut)
                except:
                    pass

            if i == 0:
                returnSet = set(candidateNodes)
            else:
                returnSet = returnSet.intersection(set(candidateNodes))

        return returnSet

    def get_graph(self):
        nodeCoords = []

        count = 0
        while count < self.number_of_nodes:
            coord = (random.random(), random.random(), random.random())
            nodeCoords.append(coord)
            count += 1

        # Bin per coordinate
        binPerCoord = self.bin_count
        distanceMeasure = float(1) / binPerCoord

        binContents = [{}, {}, {}]

        for i in range(len(nodeCoords)):
            node = nodeCoords[i]

            for j in range(3):
                ind = int(floor(node[j] * binPerCoord))

                if ind not in binContents[j]:
                    binContents[j][ind] = [i]
                else:
                    binContents[j][ind].append(i)


        # Identify the distances in reduced indexes
        pairwiseDists = {}
        neighborCount = 1
        candidateEdges = []

        while True:
            for i in range(len(nodeCoords)):
                candids = self.__identifyCandidates(nodeCoords[i], binContents, neighborCount, binPerCoord)

                for index in candids:
                    if index <> i:
                        distanceSum = 0
                        for j in range(3):
                            distanceSum += (nodeCoords[i][j] - nodeCoords[index][j]) ** 2
                        distance = sqrt(distanceSum)

                        if distance < (distanceMeasure * neighborCount):
                            if i < index:
                                if i not in pairwiseDists:
                                    pairwiseDists[i] = {}

                                pairwiseDists[i][index] = distance
                            else:
                                if index not in pairwiseDists:
                                    pairwiseDists[index] = {}
                                pairwiseDists[index][i] = distance

            for index1 in pairwiseDists:
                for index2 in pairwiseDists[index1]:
                    candidateEdges.append((index1, index2, pairwiseDists[index1][index2]))

            if len(candidateEdges) < self.number_of_edges:
                neighborCount += 1
            else:
                candidateEdges = sorted(candidateEdges, key=lambda edge: edge[2])
                candidateEdges = candidateEdges[:self.number_of_edges]  #
                break

        # Create the networkX object and return
        generatedGraph = nx.Graph()

        generatedGraph.add_nodes_from(range(self.number_of_nodes))

        for edge in candidateEdges:
            generatedGraph.add_edge(edge[0], edge[1])

        return generatedGraph
