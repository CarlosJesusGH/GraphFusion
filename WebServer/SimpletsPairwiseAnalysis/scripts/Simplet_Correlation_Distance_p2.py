#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created by Noel Malod-Dognin, 2018
"""

import numpy as np
from scipy.stats import spearmanr
import math
import sys
import matplotlib.pyplot as plt


# Load the SDV signature of a simplicial complex (pointed by path)
def read_count(path):
	data = []
	ifile = open(path, 'r')
	for line in ifile.readlines():
		lspt = line.strip().split(';')
		if len(lspt)> 2:
			sdv = [float(e) for e in lspt[1:-1]]
			data.append(sdv)
	return data



# Compute the SCM of a simplicial complex, based on its SDV signature file (pointed by path2count)
def Make_SCM(path2count):
	dvs = read_count(path2count)
	
	dvs_np = np.array(dvs)
	#print dvs_np.shape
	orbit_np = np.transpose(dvs_np)
	nb_orbit = len(orbit_np)
	
	table = [[1. for j in range(nb_orbit)] for i in range(nb_orbit)]
	for i in range(nb_orbit):
		for j in range(i+1,nb_orbit):
			pcc = spearmanr(orbit_np[i], orbit_np[j])
			pcc0 = pcc[0]
			if np.isnan(pcc0):
				pcc0 = 0.
			table[i][j] = pcc0
			table[j][i] = pcc0
	nptable = np.array(table)
	return nptable

# Compute the distance between two SCMs
def SCD(scm1, scm2):
	dist = 0.
	n = len(scm1)
	for i in range(n):
		for j in range(i+1, n):
			d = scm1[i][j] - scm2[i][j]
			dist += d*d
	return math.sqrt(dist)


	
	
# Example of usage	
if __name__ == '__main__':
	if len(sys.argv) <> 3:
		print "Usage: python Simplet_Correlation_Distance.py <sdv_file1> <sdv_file2>"
		exit(1)
	
	sdv_file1 = sys.argv[1]
	sdv_file2 = sys.argv[2]
	
	SCM1 = Make_SCM(sdv_file1)
	SCM2 = Make_SCM(sdv_file2)
	
	distance = SCD(SCM1, SCM2)
	print "Distance: ", distance

def get_distance(sdv_file1, sdv_file2):
	SCM1 = Make_SCM(sdv_file1)
	SCM2 = Make_SCM(sdv_file2)
	distance = SCD(SCM1, SCM2)
	return distance