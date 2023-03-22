#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created by Noel Malod-Dognin, 2018
"""

import numpy as np
import sys
import math

#Simplet orbit weigths
oi = [1,2,2,2,2,3,4,3,3,3,4,4,3,4,4,4,4,4,4,5,4,4,4,3,4,3,4,4,4,3,3,3]
wi = [1.-(math.log(float(i))/math.log(32.)) for i in oi]
swi = sum(wi)


# Compute the distance between the SDV signatures of two nodes
def SDV_Distance2(u,v):
	SDI = 0.
	lswi = 0.
	for i in range(32):
		ui = u[i]
		vi = v[i]
		if ui <> 0. or vi<> 0.:
			SDI += wi[i]*abs(math.log(ui+1.)-math.log(vi+1.))/(math.log(max(ui,vi)+2.))
			lswi += wi[i]
	return SDI/lswi


# Load the SDV signatures of a simplicial complex (pointed by path)
def read_count(path):
	dvs = []
	genes = []
	ofile = open(path,'r')
	for line in ofile.readlines():
		lspt = line.strip().split(';')
		if len(lspt)>1:
			sdv = [float(e) for e in lspt[1:-1]]
			dvs.append(sdv)
			genes.append(lspt[0])
			if sum(sdv)==0:
				print "Gene %s has empty SDV"%(lspt[0])
	return genes, dvs



# Example of usage	
if __name__ == '__main__':
	if len(sys.argv) <> 3:
		print "Usage: python SDV_Distance.py <input sdv_file> <output_distance_file>"
		print "Warning, this script computes distances, i.e., 1 - similarity"
		exit(1)
	
	#loading data
	path2count = sys.argv[1]
	genes, dvs = read_count(path2count)
	
	#applying distance between data
	n = len(genes)
	data = np.zeros((n,n))
	
	full = (n*(n-1.))/2
	perc = int(full/100.)
	
	cnt = 0
	for i in range(n):
		data[i][i] = 1.
		for j in range(i+1, n):
			cnt += 1
			
			if cnt%perc == 0:
				print "%i percent done"%(int(100.*cnt/float(full)))
			dst = SDV_Distance2(dvs[i],dvs[j])
			data[i][j] = dst*dst
			data[j][i] = dst*dst
	
	#outputing distances
	ofname = sys.argv[2]
	ofile = open(ofname, 'w')
	for i in range(n):
		ofile.write("%s"%(genes[i]))
		for j in range(n):
			ofile.write("\t%f"%(data[i][j]))
		ofile.write("\n")
	ofile.close()



