"""
From the iCell paper:
 This integrated network is obtained by thresholding the matrix G  GT by using rowand column-centric rules to preserve only the top 1% of the strongest relationships in each row and column.
 In the co-clustering interpretation of NMTF, each row of G corresponds to a gene, each column of G corresponds to a cluster, and the value G[u][i] (in row u, column i) is the closeness of gene u to cluster i.
"""

import sys
# import operator
#import networkx as nx
import math
from scipy.stats import hypergeom
import numpy as np
# import scipy.stats as ss
# import matplotlib.pyplot as plt
import networkx as nx
from scipy.cluster.vq import vq, kmeans, kmeans2, whiten
# import scipy.cluster.hierarchy as sch
import os.path


def umin(L):
	if len(L)>0:
		return min(L)
	return 0.

def umax(L):
	if len(L)>0:
		return max(L)
	return 0.

def uavg(L):
	if len(L)>0:
		return sum(L)/float(len(L))
	return 0.

# Benjamini-Hochberg p-value correction for multiple hypothesis testing
def p_adjust_bh(p):
    p = np.asfarray(p)
    by_descend = p.argsort()[::-1]
    by_orig = by_descend.argsort()
    steps = float(len(p)) / np.arange(len(p), 0, -1)
    q = np.minimum(1, np.minimum.accumulate(steps * p[by_descend]))
    return q[by_orig]
    #return p

# Cosine similarity between two vectors
def cosine_similarity(v1,v2):
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)


# Load gene list
def Load_Gene_list(filename):
	Glist = []
	ofile = open(filename, 'r')
	#skip file header line
	ofile.readline()
	for line in ofile.readlines():
		gene = line.strip().split()[0]
		Glist.append( gene )
	ofile.close()
	#safety test
	Gset = set(Glist)
	if len(Gset) <> len(Glist):
		print "!!!! Duplicated genes in gene list"
	return Glist

# Load a matrix
def Load_Matrix(filename):
	G = []
	ofile = open(filename, 'r')
	for line in ofile.readlines():
		row = [float(i) for i in line.strip().split('\t')]
		G.append( row )
	ofile.close()
	return np.array(G)



"""
	Main code starts here
"""


# idir = './Res_Int/'
# odir = './Integrated_Nets/'
# idir = './input/'
# odir = './output/'
# idir = './'
# odir = './'

# lst = ['breast_glandular-cells', 'breast-cancer', 'prostate_glandular-cells', 'prostate-cancer', 'lung_pneumocytes', 'lung-cancer', 'colon_glandular-cells', 'colorectal-cancer']
# lst = [sys.argv[1], sys.argv[2]]
genelist_filepath = sys.argv[1]
factor_filepath = sys.argv[2]
output_filename = sys.argv[3]

# for tissue in lst:

#load genelist, G matrix and building raw integrated network
# Glist = Load_Gene_list(idir+tissue+"_iCell_genelist.csv")
Glist = Load_Gene_list(genelist_filepath)
nb_gene = len(Glist)
# G = Load_Matrix(idir+tissue+'_iCell_G_k50.csv')
# G = Load_Matrix(idir+tissue+'_G.csv')
G = Load_Matrix(factor_filepath)
GT = np.transpose(G)
Raw_Net = np.dot(G,GT)

#thresholding integrated network
ind = int( float(nb_gene)*0.99 )

#ind2 =int( float(nb_gene) - float(nb_gene)*0.01 )

Int_Net = nx.Graph()
for i in range(nb_gene):
	sorted_row = np.sort( Raw_Net[i], kind='mergesort')
	val  = sorted_row[ind]
	genei = Glist[i]
	for j in range(nb_gene):
		genej = Glist[j]	
		if (genei <> genej) and Raw_Net[i][j]>= val:
			if not(Int_Net.has_edge(genei, genej)):
				Int_Net.add_edge(genei, genej, weigth=Raw_Net[i][j])

# print "%s: Integrated net has %i nodes and %i edges"%(tissue, Int_Net.number_of_nodes(), Int_Net.number_of_edges())
print "Integrated net has %i nodes and %i edges"%(Int_Net.number_of_nodes(), Int_Net.number_of_edges())
# nx.write_edgelist(Int_Net, odir+tissue+'_iCell_100.edgelist', data=['weight'])
nx.write_edgelist(Int_Net, output_filename, data=['weight'])