#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created by Noel Malod-Dognin, 2018
"""

import numpy as np
import math
import sys


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
	

# Compute the facet distribution of a simplicial complex (pointed by path2sc)
def Make_FD(path2sc):
	sc = read_sc(path2sc)
	nb_e = len(sc)
	k = 0;
	for i in range(nb_e):
		dd = len(sc[i])
		if dd>k:
			k=dd
	fd = np.zeros(k+1)
	for i in range(nb_e):
		dd = len(sc[i])
		fd[dd]+=1.
	fd=fd/float(nb_e)
	return fd


# Compute the distance between two facet distributions
def FD_dist(fd1, fd2):
	dist = 0.
	n1=len(fd1)
	n2=len(fd2)
	
	for i in range(min(n1,n2)):
		d = fd1[i] - fd2[i]
		dist += d*d
	if n1 < n2:
		for i in range(n1,n2):
			d = fd2[i]
			dist += d*d
	if n1 > n2:
		for i in range(n2,n1):
			d = fd1[i]
			dist += d*d
	return math.sqrt(dist)


		
# Example of usage	
if __name__ == '__main__':
	# if len(sys.argv) <> 3:
  if len(sys.argv) != 3:
		# print "Usage: python Facet_Distribution_Distance.py <sc_file1> <sc_file2>"
    print("Usage: python Facet_Distribution_Distance.py <sc_file1> <sc_file2>")
    exit(1)
	
  sc_file1 = sys.argv[1]
  sc_file2 = sys.argv[2]
	
  fd1 = Make_FD(sc_file1)
  fd2 = Make_FD(sc_file2)
	
  distance = FD_dist(fd1, fd2)
  # print "Distance: ", distance
  print("Distance: ", distance)
