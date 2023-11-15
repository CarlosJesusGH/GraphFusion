#!/usr/bin/env python



import sys
import os

import math
import numpy as np
# import matplotlib.pyplot as plt

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

def Load_glist(gfname):
	nodes = []
	nodemap = {}
	i = 0
	ifile = open(gfname, 'r')
	for line in ifile.readlines():
		lspt = line.strip().split()
		if len(lspt) > 0:
			gene = lspt[0]
			nodes.append(gene)
			nodemap[gene] = i
			i += 1
	return [nodes, nodemap]

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
	#print ppi_name, " has ", len(vertices), " gdvs"
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

def outputpairs(Data, ofname):
	verts = Data[0]
	sigs = Data[1]
	ofile = open(ofname, "w")
	nb_pairs = len(verts)*(len(verts)-1)/2.
	done = 0.
	prev_perc = 0
	for i in range(len(verts)):
		vi = verts[i]
		sigi = sigs[i]
		for j in range(i+1, len(verts)):
			vj = verts[j]
			sigj = sigs[j]
			score =  gds_sim(sigi, sigj)
			ofile.write("%s\t%s\t%f\n"%(vi, vj, score))
			done += 1.
			perc = int(100.*done/nb_pairs)
			if perc > prev_perc:
				print perc, " % done..."
			prev_perc = perc
	ofile.close()
	return 0



#load expressed nodes cancer:
gcfname = sys.argv[1]
gclist, gcmap = Load_glist(gcfname)

#load expressed nodes normal:
gnfname = sys.argv[2]
gnlist, gnmap = Load_glist(gnfname)

# get commonly expressed genes
glist = list( set(gclist) & set(gnlist) )
gmap = {}
for i in range(len(glist)):
	gmap[glist[i]] = i
nb_genes = len(glist)
print "%i commonly expressed genes"%(nb_genes)


#load cancer data (.ndump2)
cfname = sys.argv[3]
cnode, cmap, csigs = Load_ndump(cfname)

#load normal tissue data (.ndump2)
nfname = sys.argv[4]
nnode, nmap, nsigs = Load_ndump(nfname)

gdvsims = np.zeros(nb_genes)
for i in range(nb_genes):
	gene = glist[i]
	if gene in cmap:
		id_c = cmap[gene]
		sig_c = csigs[id_c]
	else:
		sig_c = np.zeros(16)
	if gene in nmap:
		id_n = nmap[gene]
		sig_n = nsigs[id_n]
	else:
		sig_n = np.zeros(16)
	sim = gds_sim(sig_c, sig_n)
	gdvsims[i] = 1.-sim

ofile = open(sys.argv[5], 'w')
for i in range(nb_genes):
	gene = glist[i]
	sim = gdvsims[i]
	ofile.write("%s\t%s\n"%(gene, str(sim)))
ofile.close()

#plt.hist(gdvsims, bins=100)
#plt.title("Rewired genes in %s cancer"%(sys.argv[6]))
#plt.xlabel('GDV distance')
#plt.ylabel('#Genes')
#plt.savefig("%s_gdvs_dist.svg"%(sys.argv[6]))


