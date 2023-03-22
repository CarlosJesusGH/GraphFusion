#!/usr/bin/env python
'''
Run as: ./generate_DiRandomGraphs.py
'''

import sys
import os
sys.path.append("/vol/bio-nets/packages/networkx-1.6/")
import networkx as nx
import random
from math import floor
from math import sqrt
import multiprocessing
from networkx.generators.classic import empty_graph, path_graph 
from networkx.utils import discrete_sequence
import math

DG=nx.DiGraph()

####NOTE FOR NOEL: Here you will find the functions for generating GEO, 
# GEOGD and directed SF. For directed ER I used python implementation (it is comented out). 
# Generaly ignore stuff that is commented out because I was trying out different stuff 
# and this remained there....You can use this to modify the GEO, GEOGD and directed 
# SF models as you wish...
# Also, for the SF models refer to the notations for the parameters from the supplementary...

"""
for i in range(1,31):
    
    DG=nx.erdos_renyi_graph(500,0.005,directed=True)
    nx.write_edgelist(DG, "ER_500_005-graph"+str(i)+".edgelist.txt",data=False)
    
    DG=nx.erdos_renyi_graph(2000,0.005,directed=True)
    nx.write_edgelist(DG, "ER_2000_005-graph"+str(i)+".edgelist.txt",data=False)
    DG=nx.erdos_renyi_graph(5000,0.005,directed=True)
    nx.write_edgelist(DG, "ER_5000_005-graph"+str(i)+".edgelist.txt",data=False)
    
    DG=nx.erdos_renyi_graph(500,0.01,directed=True)
    nx.write_edgelist(DG, "ER_500_01-graph"+str(i)+".edgelist.txt",data=False)
    
    DG=nx.erdos_renyi_graph(2000,0.01,directed=True)
    nx.write_edgelist(DG, "ER_2000_01-graph"+str(i)+".edgelist.txt",data=False)
    DG=nx.erdos_renyi_graph(5000,0.01,directed=True)
    nx.write_edgelist(DG, "ER_5000_01-graph"+str(i)+".edgelist.txt",data=False)
    """

#GEOMETRIC GRAPHS
# Identify the candidate nodes in the bins to search for (reduced space)
def identifyCandidates(node, binContents, neighborCount, binPerCoord):
	
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

# Generates a geometric network
def generateGeometric(nodeCount, edgeCount, binCount):
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
			candids = identifyCandidates(nodeCoords[i], binContents, neighborCount, binPerCoord)
		
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

# Generates a geometric network with GD
def generateGeoGD(nodeCount, edgeCount, binCount):
	
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
			candids = identifyCandidates(nodeCoords[i], binContents, neighborCount, binPerCoord)
	
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

# Generates a SFGD network
def generateSFGD(nodeCount, edgeCount, p, q, ec):
	qstep = 0
	
	while q >= 0 and q <= 1:
		avg_nodes = 0
		avg_edges = 0
		
		for i in range(ec):
			# Create the graph with an edge
			graph = nx.DiGraph()
			graph.add_edge(0, 1)
			
			for i in range(2, nodeCount):
				RND = random.choice(graph.nodes())
				
				# Add the new node
				graph.add_node(i)
				
				# Add the edge between RND and new node with probability p, but the decide on directionality with 50% chances in favour both options
				choose_prob = random.random()
				if choose_prob <= p:
                                        num=random.random() #generise random broj u [0.0, 1.0), pa je dobra podjela [0.0,0.5) i [0.5,1.0)
                                        if num < 0.5:
                                            graph.add_edge(i,RND)
                                        else:
                                            graph.add_edge(RND,i)
					
				
				# Connect the node 'i' to all the neighbours of RND
				for succ in graph.successors(RND):
					if succ <> i:
						graph.add_edge(i, succ)
				for pred in graph.predecessors(RND):
					if pred <> i:
						graph.add_edge(pred, i)
				
				# Mutate the new node by removing the edges
				successors_i = graph.successors(i)
				predecessors_i = graph.predecessors(i)
                                list_of_neigbors=list()
				for successor in successors_i:
                                    list_of_neigbors.append(successor)
				for predecessor in predecessors_i:
                                    list_of_neigbors.append(predecessor)

				for neigbor in list_of_neigbors:
					if neigbor <> RND:
						choose_prob = random.random()
                                                if choose_prob < q:
                                                    if neigbor in successors_i and neigbor in predecessors_i:# Remove the edge (i - sucessor) or the edge (predecessor - i) with equal probabilities
                                                        num=random.random() #generise random broj u [0.0, 1.0), pa je dobra podjela [0.0,0.5) i [0.5,1.0)
                                                        if num < 0.5:
                                                            graph.remove_edge(i,neigbor)
                                                        else:
                                                            graph.remove_edge(neigbor,i)
                                                    else: 
                                                        if neigbor in successors_i:# Remove the edge (i - sucessor)
							    graph.remove_edge(i, neigbor)
                                                        if neigbor in predecessors_i:# Remove the edge (predecessor - i)
							    graph.remove_edge(neigbor,i)

			
			if graph.number_of_edges() >= (0.99 * edgeCount) and graph.number_of_edges() <= (1.01 * edgeCount):
				return graph
			
			avg_edges += float(graph.number_of_edges()) / ec
		
		if avg_edges < edgeCount:
			if qstep == 0:
				qstep = -0.1
			elif qstep > 0:
				qstep = (-1 * qstep) / 2
		else:
			if qstep == 0:
				qstep = 0.1
			elif qstep < 0:
				qstep = (-1 * qstep) / 2
		
		q += qstep
	
	print 'ERROR! No SFGD graph could be generated'
	exit(0)

###SF-BA generalized directed graph

def _directed_scale_free_graph(n, num_of_edges, alpha, beta, gamma, delta_in, delta_out, create_using=None, seed=None):
   
    def _choose_node(G,distribution,delta):
        cumsum=0.0
        # normalization 
        psum=float(sum(distribution.values()))+float(delta)*len(distribution)
        r=random.random()
        for i in range(0,len(distribution)):
            cumsum+=(distribution[i]+delta)/psum
            if r < cumsum:  
                break
        return i

    #find size of seed network
    B=n-(beta/float(alpha+gamma))
    D=math.pow(B, 2)-4*(num_of_edges - float(beta*n)/(alpha+gamma))
    m=int((B-math.sqrt(D))/2)
    
    #m_corr=int(float(num_of_edges-(float(beta*n)/(alpha+gamma)))/n)
    #m=int(float(num_of_edges-(float(beta*(n-m_corr))/(alpha+gamma)))/(n-m_corr))
    #print m
    if create_using is None:
        # start with 3-cycle
        
        H=path_graph(m)
        G=nx.DiGraph(H)
    else:
        # keep existing graph structure?
        G = create_using
        if not G.is_directed():
            raise nx.NetworkXError(\
                  "MultiDiGraph required in create_using")

    if alpha <= 0:
        raise ValueError('alpha must be >= 0.')
    if beta < 0:
        raise ValueError('beta must be <>=0.')
    if gamma <= 0:
        raise ValueError('beta must be >= 0.')

    if alpha+beta+gamma !=1.0:
        raise ValueError('alpha+beta+gamma must equal 1.')
        
    
    # seed random number generated (uses None as default)
    random.seed(seed)

    
    while len(G)<n:
        r = random.random()
        # random choice in alpha,beta,gamma ranges
        if r<alpha:
            # alpha
            # add new node v
            v = len(G) 
            # choose m nodes w according to in-degree and delta_in
            counter=0
            while counter<m:
                w = _choose_node(G, G.in_degree(),delta_in)
                if (v,w) not in G.edges():
                    G.add_edge(v,w)
                    counter=counter+1
        elif r < alpha+beta:
            # beta
            # choose v according to out-degree and delta_out
            v = _choose_node(G, G.out_degree(),delta_out)
            # choose w according to in-degree and delta_in
            w = _choose_node(G, G.in_degree(),delta_in)
            G.add_edge(v,w)
        else:
            # gamma
            w = len(G)
            # choose m nodes v according to out-degree and delta_out
            counter=0
            while counter<m:
                v = _choose_node(G, G.out_degree(),delta_out)
                if (v,w) not in G.edges():
                    G.add_edge(v,w)
                    counter=counter+1
                      
       
        
    return G

# Worker
def worker(list_of_indexes_per_processor,c):
    for i in list_of_indexes_per_processor:

        ### usage: network = generateSFGD(nodeCount, edgeCount, p, q, experimentCount)
        ###usage: graph = _directed_scale_free_graph(nodeCount,edgeCount,0.5,0,0.5,0,0, create_using=None,seed=None)
        """
        DG=generateSFGD(500, 2500,0.5,0.5, 500)
        nx.write_edgelist(DG, "SFGD_500_01-graph"+str(i)+".edgelist.txt",data=False)
        DG=generateSFGD(500, 1250,0.5,0.5, 500)
        nx.write_edgelist(DG, "SFGD_500_005-graph"+str(i)+".edgelist.txt",data=False)
        
        DG=generateSFGD(1000, 10000, 0.5,0.5, 500)
        nx.write_edgelist(DG, "SFGD_1000_01-graph"+str(i)+".edgelist.txt",data=False)
        DG=generateSFGD(1000, 5000, 0.5,0.5, 500)
        nx.write_edgelist(DG, "SFGD_1000_005-graph"+str(i)+".edgelist.txt",data=False)

        DG=generateSFGD(2000, 40000,0.5,0.5, 500)
        nx.write_edgelist(DG, "SFGD_2000_01-graph"+str(i)+".edgelist.txt",data=False)
        DG=generateSFGD(2000, 20000,0.5,0.5, 500)
        nx.write_edgelist(DG, "SFGD_2000_005-graph"+str(i)+".edgelist.txt",data=False)
        """
        DG=_directed_scale_free_graph(500, 2500,0.5,0,0.5,0,0, create_using=None,seed=None)
        nx.write_edgelist(DG, "SF_500_01-graph"+str(i)+".edgelist.txt",data=False)
        DG=_directed_scale_free_graph(500, 1250,0.4,0.2,0.4,0,0, create_using=None,seed=None)
        nx.write_edgelist(DG, "SF_500_005-graph"+str(i)+".edgelist.txt",data=False)
        
        DG=_directed_scale_free_graph(1000, 10000,0.5,0,0.5,0,0, create_using=None,seed=None)
        nx.write_edgelist(DG, "SF_1000_01-graph"+str(i)+".edgelist.txt",data=False)
        DG=_directed_scale_free_graph(1000, 5000,0.5,0,0.5,0,0, create_using=None,seed=None)
        nx.write_edgelist(DG, "SF_1000_005-graph"+str(i)+".edgelist.txt",data=False)

        DG=_directed_scale_free_graph(2000, 40000,0.5,0,0.5,0,0, create_using=None,seed=None)
        nx.write_edgelist(DG, "SF_2000_01-graph"+str(i)+".edgelist.txt",data=False)
        DG=_directed_scale_free_graph(2000, 2000,0.5,0,0.5,0,0, create_using=None,seed=None)
        nx.write_edgelist(DG, "SF_2000_005-graph"+str(i)+".edgelist.txt",data=False)
        """
        DG=generateGeometric(5000, 250000, 5000)
        nx.write_edgelist(DG, "GEO_5000_01-graph"+str(i)+".edgelist.txt",data=False)
        
        DG=generateGeoGD(1000, 10000, 1000)
        nx.write_edgelist(DG, "GEOGD_1000_01-graph"+str(i)+".edgelist.txt",data=False)
        DG=generateGeoGD(2000, 40000, 2000)
        nx.write_edgelist(DG, "GEOGD_2000_01-graph"+str(i)+".edgelist.txt",data=False)
        DG=generateGeoGD(5000, 250000, 5000)
        nx.write_edgelist(DG, "GEOGD_5000_01-graph"+str(i)+".edgelist.txt",data=False)
        
        DG=generateGeometric(500, 2500, 500)
        nx.write_edgelist(DG, "GEO_5000_01-graph"+str(i)+".edgelist.txt",data=False)
        DG=generateGeometric(500, 1250, 500)
        nx.write_edgelist(DG, "GEO_5000_005-graph"+str(i)+".edgelist.txt",data=False)

        DG=generateGeoGD(500, 2500, 500)
        nx.write_edgelist(DG, "GEOGD_5000_01-graph"+str(i)+".edgelist.txt",data=False)
        DG=generateGeoGD(500, 1250, 500)
        nx.write_edgelist(DG, "GEOGD_5000_005-graph"+str(i)+".edgelist.txt",data=False)
        """

# -----------------
### MAIN ###
jobs=[]
# CPU_COUNT = int(0.8*multiprocessing.cpu_count())
CPU_COUNT = 1

counter = 0
alloc = [list() for x in range(CPU_COUNT)]
for j in range(1,31):
    cpu = counter%CPU_COUNT
    alloc[cpu].append(j)
    counter+=1

## pokrece procese
for c in range(CPU_COUNT):
    p = multiprocessing.Process(target=worker,args=(alloc[c],c))
    jobs.append(p)
    p.start()    

## ceka na procese da svi zavrse
for j in jobs:
    j.join()  


