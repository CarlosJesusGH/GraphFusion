#!/usr/bin/env python

import sys
import os
import numpy as np
import math
from scipy.stats import hypergeom
import scipy.stats as ss

ICELL_GDV_FILE_NAME = sys.argv[1]
GDV_GENELIST_FILENAME = sys.argv[2]
GDV_SIMS_FILENAME = sys.argv[3]

cancer_lst = []
for task_dir in sys.argv[4:]:
	cancer_lst.append(task_dir)
print("cancer_lst:", cancer_lst)

print "\nStep 1: Loading expression data"

#getting gene expression from all cancer

ifile = open(GDV_GENELIST_FILENAME, 'r')
sub_gene_lst = []
sub_gene_map = {}
cnt = 0
for line in ifile.readlines():
	lspt = line.strip().split()
	if len(lspt)>0:
		gene = lspt[0]
		sub_gene_lst.append(gene)
		sub_gene_map[gene] = cnt
		cnt += 1
ifile.close()

nb_sgene = len(sub_gene_lst)
print "      : %i genes are expressed in all cells"%(nb_sgene)

# -------------------------------------------------------------------

print "\nStep 2: Computing Avg. GDV similarities"

#the 11 non redundant 2- to 4-node graphlets
nr_orbits = [0,1,2,4,5,6,7,8,9,10,11]
# the orbit importance
oi = [1, 2, 2, 2, 3, 4, 3, 3, 4, 3, 4, 4]
sum_oi = 0.
sum_wi = 0.

weights   = [1.-math.log(oi[i])/math.log(11.) for i in range(12)]
for i in nr_orbits:
	sum_oi += float(oi[i])
	sum_wi += weights[i]

def Load_ndump(ifname):
	vertices = []
	vmap = {}
	i = 0
	sigs = []
	ofile = open(ifname, "r")
	for line in ofile.readlines():
		lspt = line.strip().split()
		if len(lspt)> 12:
			gdv=  []
			vertices.append( lspt[0] )
			vmap[lspt[0]] = i
			i+=1
			for j in range(1, 16):
				gdv.append(float(lspt[j]))
			sigs.append(gdv)
	ofile.close()
	return [vertices, vmap, sigs]

# compute the GDV similarity using the non-redundant 2-to 4-node graphlet degrees
def gds_sim(U, V):
	D = 0.
	for i in nr_orbits:
		wi = weights[i]
		Di = wi * abs( math.log(U[i]+1.) - math.log(V[i]+1.) ) / math.log( max(U[i], V[i]) +2. )
		D+= Di
	D = D/sum_wi
	return D

gene_gdvs = [0 for i in range(nb_sgene)]

cnt = 1
nbpairs = float(len(cancer_lst)*(len(cancer_lst)-1))/2.
for i in range(len(cancer_lst)):
	# vertices_i, vmap_i, sigs_i = Load_ndump("./Integrated_Nets/%s_iCell_100.ndump2"%(cancer_lst[i]))
	vertices_i, vmap_i, sigs_i = Load_ndump("../%s/%s"%(cancer_lst[i], ICELL_GDV_FILE_NAME))
	for j in range(i+1, len(cancer_lst)):
		vertices_j, vmap_j, sigs_j = Load_ndump("../%s/%s"%(cancer_lst[j], ICELL_GDV_FILE_NAME))
		print "      : Processing pair %i / %i"%(cnt, int(nbpairs))
		for k in range(nb_sgene):
			gene_k = sub_gene_lst[k]
			if gene_k in vmap_i:
				gdv_ki = sigs_i[vmap_i[gene_k]]
			else:
				gdv_ki = [0 for u in range(16)]
			if gene_k in vmap_j:
				gdv_kj = sigs_j[vmap_j[gene_k]]
			else:
				gdv_kj = [0 for u in range(16)]
			gdvs_kij = 1.-gds_sim(gdv_ki, gdv_kj)
			norm_kij = gdvs_kij/nbpairs
			gene_gdvs[k] += norm_kij
		cnt +=1

# minx = min(gene_gdvs)
# my_hist=np.histogram(gene_gdvs, 50)
# x2=[]
# y2=[]
# for i in range(len(my_hist[0])):
# 	x2.append(my_hist[1][i])
# 	y2.append(my_hist[0][i])


ofile = open(GDV_SIMS_FILENAME,"w")
for k in range(nb_sgene):
	gene_k = sub_gene_lst[k]
	gdvs_k = gene_gdvs[k]
	ofile.write("%s\t%f\n"%(gene_k, gdvs_k))
ofile.close()


#load mutated genes


gdvsmap = {}
for k in range(nb_sgene):
	gene_k = sub_gene_lst[k]
	gdvs_k = gene_gdvs[k]
	if gdvs_k not in gdvsmap:
		gdvsmap[gdvs_k] = []
	gdvsmap[gdvs_k].append(gene_k)
keys = list(reversed(sorted(gdvsmap.keys())))
sorted_rewired = []
for key in keys:
	for elem in gdvsmap[key]:
		sorted_rewired.append(elem)

# U = 500
#most_rewired = set( sorted_rewired[:U] )
# least_rewired = set( sorted_rewired[len(sorted_rewired)-U:] )
