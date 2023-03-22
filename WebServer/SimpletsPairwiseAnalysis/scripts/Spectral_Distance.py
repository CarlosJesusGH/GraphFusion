#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created by Noel Malod-Dognin, 2018
"""

import numpy as np
import math
import sys
import numpy.linalg as LA

# Load the facets of a simplicial complex (pointed by path)
def read_sc(path):
	data = []
	ifile = open(path, 'r')
	for line in ifile.readlines():
		lspt = line.strip().split()
		if len(lspt)>= 2:
			edge = set(lspt)
			data.append(edge)
	ifile.close()
	return data


# Compute the list of eigen-values of the laplacian matrix of a simplicial complex (pointed by path2sc)
def Make_Eig(path2sc):
	sc = read_sc(path2sc)
	nodes = set()
	for s in sc:
		nodes.update(s)
	corresp = {}
	for n in nodes:
		corresp[n] = len(corresp)
	len_e = len(sc)
	len_n = len(nodes)
	H = np.zeros((len_n, len_e))
	for ss in range(len(sc)):
		s=sc[ss]
		for i in s:
			ii = corresp[i]
			H[ii][ss] = 1.
	Dv = np.sum(H,axis=1,keepdims=True)    
	m,n = H.shape

	A = np.dot(H,H.T) - np.diag(Dv[:,0])
	Dinv = np.divide(1,np.sqrt(Dv))
	L = 0.5*(np.identity(m) - np.multiply(Dinv,np.multiply(A,Dinv.T)))
	eigvals, eig_vect = LA.eigh(L)
	eigvals_sorted = sorted(eigvals, reverse=True)
	return eigvals_sorted

# Compute the distance between two lists of eigen-values
def eig_dist(eig1, eig2):
	dist = 0.
	n1=len(eig1)
	n2=len(eig2)
	
	for i in range(min(n1,n2)):
		d = eig1[i] - eig2[i]
		dist += d*d
	if n1 < n2:
		for i in range(n1,n2):
			d = eig2[i]
			dist += d*d
	if n1 > n2:
		for i in range(n2,n1):
			d = eig1[i]
			dist += d*d
	return math.sqrt(dist)


	
# Example of usage	
if __name__ == '__main__':
	if len(sys.argv) <> 3:
		print "Usage: python Spectral_Distance.py <sc_file1> <sc_file2>"
		exit(1)
	
	sc_file1 = sys.argv[1]
	sc_file2 = sys.argv[2]
	
	Eig1 = Make_Eig(sc_file1)
	Eig2 = Make_Eig(sc_file2)
	
	distance = eig_dist(Eig1, Eig2)
	print "Distance: ", distance