# -*- coding: utf-8 -*-

import os
import sys
import networkx as nx
import scipy.stats as ss
import numpy.linalg as nl
import numpy as np
import math



def load_go_annotations(genelist,fname):
	annotations = {}
	for gene in genelist:
		annotations[gene] = set()
	go_stats = {}
	fread = open(fname, "r")
	for line in fread.readlines():
		lsplit = line.strip().split()
		gene = lsplit[0]
		goterm = lsplit[1]
		if gene not in annotations:
			print "invalid gene"
			exit()
		annotations[gene].add(goterm)
		if goterm not in go_stats:
			go_stats[goterm] = 0
		go_stats[goterm] += 1
	selected_annot = set()
	for go in go_stats:
		if go_stats[go] >= 5 and go_stats[go] < len(genelist)/2.:
			selected_annot.add(go)
	print "Total go = ",str(len(go_stats)), ", selected = ", str(len(selected_annot))
	return [annotations, selected_annot]

def load_gdvs(sigfname):
	sig = {}
	k= 73
	fRead = open(sigfname, 'r')	
	for line in fRead:
		lsplit = line.strip().split(' ')
		if len(lsplit) > k:
			node = lsplit[0]
			gdv = [float(val) for val in lsplit[1:(k+1)]]
			sig[node] = gdv
	return sig

def make_matrices(genelist, annotations, selected_annot, gdvs, gomatrixfname, gdvmatrixfname, use_log=False):
	gofile = open(gomatrixfname,"w")
	#header
	gofile.write("\" \"")
	for goterm in selected_annot:
		gofile.write(",\"%s\""%(goterm))
	gofile.write("\n")
	#main
	for gene in genelist:
		gofile.write("\"%s\""%(gene))
		local_annot = annotations[gene]
		for goterm in selected_annot:
			i = 0.
			if goterm in local_annot:
				i = 1.
			gofile.write(",%s"%(str(i)))
		gofile.write("\n")
	gofile.close()
	
	#GDV matrix
	gdvfile = open(gdvmatrixfname,"w")
	#header
	gdvfile.write("\" \"")
	for g in range(73):
		gdvfile.write(",\"%s\""%(str(g)))
	gdvfile.write("\n")
	#main
	for gene in genelist:
		gdvfile.write("\"%s\""%(gene))
		local_gdv = gdvs[gene]
		for g in local_gdv:
			if use_log:
				g = math.log(g)
			gdvfile.write(",%s"%(str(g)))
		gdvfile.write("\n")
	gdvfile.close()

	

network_fname = sys.argv[1] #network filename (leda)
sig_fname = sys.argv[2] #GDV signature filename (leda)
go_fname = sys.argv[3] #go annotation filename (from PPI_get_extended_GO.py script)
matrix_fname = sys.argv[4] # output GO matrix filename

network = nx.read_leda(network_fname)
genes = network.nodes()

GOs = load_go_annotations(genes, go_fname)
SIGs = load_gdvs(sig_fname)

make_matrices(genes, GOs[0], GOs[1], SIGs, matrix_fname+"_GO.csv", matrix_fname+"_GDV.csv")

