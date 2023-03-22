__author__ = 'carlos garcia-hernandez'

from .AbstractDiGraphModelGenerator import AbstractDiGraphModelGenerator
from math import sqrt
from math import floor
import networkx as nx
import random


class DiGeometricGraphModelGenerator(AbstractDiGraphModelGenerator):
    def __init__(self, number_of_nodes, number_of_edges, bin_count):
        AbstractDiGraphModelGenerator.__init__(self, number_of_edges=number_of_edges, number_of_nodes=number_of_nodes)
        self.bin_count = bin_count

    @classmethod
    def __identifyCandidates(cls, node, binContents, neighborCount, binPerCoord):
        """Identify the candidate nodes in the bins to search for (reduced space)"""
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
        nodeCount, edgeCount, binCount = self.number_of_nodes, self.number_of_edges,self.bin_count
        # Distribute the nodes in the 3D unit space
        nodeCoords = []
        
        count = 0
        while count < nodeCount:
            coord = (random.random(), random.random(), random.random())
            nodeCoords.append(coord)
            count += 1
        
        # Bin per coordinate
        binPerCoord = binCount
        distanceMeasure = float(1) / binPerCoord
        
        binContents = [{}, {}, {}]
        
        firstCoord  = {}
        secondCoord = {}
        thirdCoord  = {}
        
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
        
        while True:
            for i in range(len(nodeCoords)):
                candids = self.__identifyCandidates(nodeCoords[i], binContents, neighborCount, binPerCoord)
            
                for index in candids:
                    if index <> i:
                        distanceSum = 0
                        for j in range(3):
                            distanceSum += (nodeCoords[i][j] - nodeCoords[index][j])**2
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

    ####ANIDA ::modified this part a bit a bit for edge direction, when adding in ''#CREATE NETWORKX OBJECT'' it should be  DIRECTED NETWORKX and take care of what is source and what is targe node	
            
            candidateEdges = []
            for index1 in pairwiseDists:
                for index2 in pairwiseDists[index1]:
                    candidateEdges.append((index1 , index2, pairwiseDists[index1][index2]))
            
            if len(candidateEdges) < edgeCount:
                neighborCount += 1
            else:
                candidateEdges = sorted(candidateEdges, key=lambda edge: edge[2])
                candidateEdges = candidateEdges[:edgeCount]#
                break
            
        # Create the networkX object and return
        generatedGraph = nx.DiGraph()
        
        generatedGraph.add_nodes_from(range(nodeCount))
        
        for edge in candidateEdges:
            num=random.random() 
            if num < 0.5:
                generatedGraph.add_edge(edge[0], edge[1])
            else:
                generatedGraph.add_edge(edge[1], edge[0])

        return generatedGraph
