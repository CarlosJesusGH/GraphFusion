__author__ = 'varun'

from .AbstractGraphModelGenerator import AbstractGraphModelGenerator
from math import sqrt
from math import floor
import networkx as nx
import random


class GeoGDGraphModelModelModelGenerator(AbstractGraphModelGenerator):
    def __init__(self, number_of_nodes, number_of_edges, bin_count):
        AbstractGraphModelGenerator.__init__(self, number_of_edges=number_of_edges, number_of_nodes=number_of_nodes)
        self.bin_count = bin_count

    @classmethod
    def __identify_candidates(cls, node, bin_contents, neighbor_count, bin_per_coord):
        return_set = set()

        for i in range(3):
            index = int(floor(node[i] * bin_per_coord))

            candidate_nodes = []
            for j in range(index - neighbor_count, index + neighbor_count + 1):
                try:
                    to_put = bin_contents[i][j]
                    candidate_nodes.extend(to_put)
                except:
                    pass

            if i == 0:
                return_set = set(candidate_nodes)
            else:
                return_set = return_set.intersection(set(candidate_nodes))

        return return_set

    def get_graph(self):
        candidate_edges = []
        while (1):
            # Generate the seed with 5 nodes many nodes from a random seed
            node_coords = []

            count = 0
            while count < 5:
                coord = (random.random(), random.random(), random.random())
                node_coords.append(coord)
                count += 1


            # Add and move the new nodes until reaching the nodeCount
            if self.bin_count == 0:
                self.bin_count = 10
            distanceMeasure = float(1) / self.bin_count
            moveDistance = sqrt(((2 * distanceMeasure) ** 2) / 3)
            binPerCoord = self.bin_count

            while count < self.number_of_nodes:
                coord = random.choice(node_coords)
                newCoord = (coord[0] + random.uniform(0, moveDistance), coord[1] + random.uniform(0, moveDistance),
                            coord[2] + random.uniform(0, moveDistance))
                node_coords.append(newCoord)
                count += 1

            # Bin per coordinate
            binContents = [{}, {}, {}]

            for i in range(len(node_coords)):
                node = node_coords[i]

                for j in range(3):
                    ind = int(floor(node[j] * binPerCoord))

                    if ind not in binContents[j]:
                        binContents[j][ind] = [i]
                    else:
                        binContents[j][ind].append(i)


            # Identify the distances in reduced indexes
            pairwiseDists = {}
            neighborCount = 1

            for i in range(len(node_coords)):
                candids = self.__identify_candidates(node_coords[i], binContents, neighborCount, binPerCoord)

                for index in candids:
                    if index <> i:
                        distanceSum = 0
                        for j in range(3):
                            distanceSum += (node_coords[i][j] - node_coords[index][j]) ** 2
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

            candidate_edges = []
            for index1 in pairwiseDists:
                for index2 in pairwiseDists[index1]:
                    candidate_edges.append((index1, index2, pairwiseDists[index1][index2]))

            if len(candidate_edges) >= self.number_of_edges:
                candidate_edges = sorted(candidate_edges, key=lambda edge: edge[2])
                candidate_edges = candidate_edges[:self.number_of_edges]
                break
            else:
                self.bin_count = floor(float(self.bin_count) / 2)

        # Create the networkX object and return
        generatedGraph = nx.Graph()

        generatedGraph.add_nodes_from(range(self.number_of_nodes))

        for edge in candidate_edges:
            generatedGraph.add_edge(edge[0], edge[1])

        return generatedGraph