__author__ = 'varun'

from .AbstractDiGraphModelGenerator import AbstractDiGraphModelGenerator
from math import sqrt
from math import floor
import networkx as nx
import random


class DiGeoGDGraphModelModelModelGenerator(AbstractDiGraphModelGenerator):
    def __init__(self, number_of_nodes, number_of_edges, bin_count):
        AbstractDiGraphModelGenerator.__init__(self, number_of_edges=number_of_edges, number_of_nodes=number_of_nodes)
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
        nodeCount, edgeCount, binCount = self.number_of_nodes, self.number_of_edges, self.bin_count
        while(1):
            # Generate the seed with 5 nodes many nodes from a random seed
            nodeCoords = []
        
            count = 0
            while count < 5:
                coord = (random.random(), random.random(), random.random())
                nodeCoords.append(coord)
                count += 1
            
            
            # Add and move the new nodes until reaching the nodeCount
            distanceMeasure = float(1) / binCount
            moveDistance = sqrt(((2*distanceMeasure) ** 2) / 3)
            binPerCoord = binCount
            
            while count <  nodeCount:
                coord = random.choice(nodeCoords)
                newCoord = (coord[0] + random.uniform(0, moveDistance), coord[1] + random.uniform(0, moveDistance), coord[2] + random.uniform(0, moveDistance))
                nodeCoords.append(newCoord)
                count += 1
                
            # Bin per coordinate
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
        
            for i in range(len(nodeCoords)):
                candids = self.__identify_candidates(nodeCoords[i], binContents, neighborCount, binPerCoord)
        
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
        
            if len(candidateEdges) >= edgeCount:
                candidateEdges = sorted(candidateEdges, key=lambda edge: edge[2])
                candidateEdges = candidateEdges[:edgeCount]
                break
            else:
                binCount = floor(float(binCount) / 2)
            
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