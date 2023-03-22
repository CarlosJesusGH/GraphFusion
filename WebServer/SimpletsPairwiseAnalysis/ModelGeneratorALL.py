__author__ = 'carlos garcia-hernandez'

from .ModelGeneratorAbstract import ModelGeneratorAbstract
import sys
import os
import networkx as nx
import numpy as np

# n = nb of nodes
# p = 1D-density
# r = nb of simplicial complexes to be generated

class ModelGeneratorALL(ModelGeneratorAbstract):
    def __init__(self, number_of_nodes, number_of_edges, oneD_density, operational_dir, model_type):
        ModelGeneratorAbstract.__init__(self, number_of_edges=number_of_edges, number_of_nodes=number_of_nodes, oneD_density=oneD_density, operational_dir=operational_dir)
        self.model_type = model_type

    def get_graph(self):
        print("Processing " + self.model_type + ", n_nodes: ", self.number_of_nodes, ", 1d-density:", self.oneD_density)
        nn, pp = self.number_of_nodes, self.oneD_density
        netname = self.operational_dir + "/" + self.model_type + "_%i_%f_%i.net"%(self.number_of_nodes, self.oneD_density, 1)
        scname = self.operational_dir + "/" + self.model_type + "_%i_%f_%i.sc"%(self.number_of_nodes, self.oneD_density, 1)
        cmd = "SimpletsPairwiseAnalysis/scripts/Make_CC %s %s"%(netname, scname)
        # for each type of model
        if self.model_type == "RCC":
            net = nx.gnp_random_graph(nn, pp)
            nx.write_edgelist(net,netname,data=False)
            os.system(cmd)
        elif self.model_type == "VRC":
            e = int(pp*((nn*(nn-1.))/2.))
            net = generateGeometric(nn, e, 10)
            nx.write_edgelist(net,netname,data=False)
            os.system(cmd)
        elif self.model_type == "SFC":
            e = int(pp*((nn*(nn-1))/2.))
            m = int(e/float(nn))+1
            net = nx.barabasi_albert_graph(nn, m)
            nx.write_edgelist(net,netname,data=False)
            os.system(cmd)
        elif self.model_type == "WSC":
            e = int(pp*((nn*(nn-1))/2.))
            m = int(e/float(nn))+1
            net = nx.watts_strogatz_graph(nn, m, 0.05)
            nx.write_edgelist(net,netname,data=False)
            os.system(cmd)
        elif self.model_type == "LM-RCC":
            # create temporal rcc
            netname_temp = self.operational_dir + "/RCC_temp.net"
            scname_temp = self.operational_dir + "/RCC_temp.sc"
            net_temp = nx.gnp_random_graph(nn, pp)
            nx.write_edgelist(net_temp,netname_temp,data=False)
            cmd = "SimpletsPairwiseAnalysis/scripts/Make_CC %s %s"%(netname_temp, scname_temp)
            os.system(cmd)
            # create lm-rcc
            facet_dist = get_facet_dist(scname_temp)
            scc = Make_LMFD(nn, facet_dist)
            write_SC(scc, scname)
        elif self.model_type == "LM-VRC":
            # create temporal vrc
            netname_temp = self.operational_dir + "/VRC_temp.net"
            scname_temp = self.operational_dir + "/VRC_temp.sc"
            e = int(pp*((nn*(nn-1.))/2.))
            net_temp = generateGeometric(nn, e, 10)
            nx.write_edgelist(net_temp,netname_temp,data=False)
            cmd = "SimpletsPairwiseAnalysis/scripts/Make_CC %s %s"%(netname_temp, scname_temp)
            os.system(cmd)
            # create lm-vrc
            facet_dist = get_facet_dist(scname_temp)
            scc = Make_LMFD(nn, facet_dist)
            write_SC(scc, scname)
        elif self.model_type == "LM-SFC":
            # create temporal sfc
            netname_temp = self.operational_dir + "/SFC_temp.net"
            scname_temp = self.operational_dir + "/SFC_temp.sc"
            e = int(pp*((nn*(nn-1))/2.))
            m = int(e/float(nn))+1
            net_temp = nx.barabasi_albert_graph(nn, m)
            nx.write_edgelist(net_temp,netname_temp,data=False)
            cmd = "SimpletsPairwiseAnalysis/scripts/Make_CC %s %s"%(netname_temp, scname_temp)
            os.system(cmd)
            # create lm-sfc
            facet_dist = get_facet_dist(scname_temp)
            scc = Make_LMFD(nn, facet_dist)
            write_SC(scc, scname)
        elif self.model_type == "LM-WSC":
            # create temporal wsc
            netname_temp = self.operational_dir + "/WSC_temp.net"
            scname_temp = self.operational_dir + "/WSC_temp.sc"
            e = int(pp*((nn*(nn-1))/2.))
            m = int(e/float(nn))+1
            net_temp = nx.watts_strogatz_graph(nn, m, 0.05)
            nx.write_edgelist(net_temp,netname_temp,data=False)
            cmd = "SimpletsPairwiseAnalysis/scripts/Make_CC %s %s"%(netname_temp, scname_temp)
            os.system(cmd)
            # create lm-wsc
            facet_dist = get_facet_dist(scname_temp)
            scc = Make_LMFD(nn, facet_dist)
            write_SC(scc, scname)
        # 
        # for all model types
        os.system("echo 'pwd:' && pwd")
        os.system("echo 'ls:' && ls " + self.operational_dir)
        # read sc file and return text
        ifile = open(scname, 'r')
        # text = ifile.readlines()
        text = ifile.read()
        ifile.close()
        return text

# ---------------------------------------------
from math import sqrt
from math import floor
import random

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
	generatedGraph = nx.Graph()
	
	generatedGraph.add_nodes_from(range(nodeCount))
	
	for edge in candidateEdges:
		generatedGraph.add_edge(edge[0], edge[1])
	
	return generatedGraph

# ---------------------------------------------

def Make_LMFD(nb_nodes, facet_dist):
	SCX = []
	nodeset = range(nb_nodes)
	Fsize = [i for i in reversed(sorted(facet_dist.keys()))]
	for s in Fsize:
		n = facet_dist[s]
		for i in range(n):
			process=True
			while process:
				new_facet = set(np.random.choice(nodeset,s,replace=False))
				valid = True
				for ss in SCX:
					if new_facet.issubset(ss):
						valid = False
						break
				if valid:
					SCX.append(new_facet)
					process=False
	
	return SCX


def load_data(fname):
	prot_set = set()
	facet_set = {}
	facet_cnt = 0
	ifile=open(fname, 'r')
	for line in ifile.readlines():
		face = set()
		lspt = line.strip().split()
		if len(lspt)>1:
			for p in lspt:
				prot_set.add(p)
				face.add(p)
			facet_set[facet_cnt] = face
			facet_cnt +=1
	ifile.close()
	print len(prot_set), " nodes, ", facet_cnt, " facets"
	return prot_set, facet_set


def get_facet_dist(fname):
	proteins, SC = load_data(fname)
	print "SC= %i proteins, %i complexes"%(len(proteins), len(SC))		
	
	
	facet_dist = {}
	for f in SC:
		l = len(SC[f])
		if l not in facet_dist:
			facet_dist[l] = 0
		facet_dist[l] += 1
	
	return facet_dist

def write_SC(SCi, fname):
	ofile = open(fname, 'w')
	for s in SCi:
		u = list(s)
		ofile.write("%s"%(u[0]))
		for i in range(1, len(u)):
			ofile.write(" %s"%(u[i]))
		ofile.write("\n")
	ofile.close()