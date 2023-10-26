"""
	Imports
"""

from doctest import testmod
import sys
import os
import math
import numpy
import time
import networkx as nx
import multiprocessing, Queue

from scipy import stats
from scipy import spatial
from scipy import linalg

from Simplet_Correlation_Distance_p2 import get_distance as SCD_get_distance
from Facet_Distribution_Distance_p2 import get_distance as FDD_get_distance

# add path to sys
# sys.path.append(os.path.join(sys.path[0], '../psb/scripts/')); # print("sys.path", sys.path)
# from ResultsAnalysis.enrichementAnalysis import *

# ---------------------------------------------------------------
"""
	Functions
"""

# Computes the euclidean distance between two correlation matrices
def computeMatrixDist_OLD(matrix1, matrix2):
	differenceSum = 0	
	for i in range(len(matrix1) - 1):
		for j in range( i + 1 , len(matrix1)):
			differenceSum += pow(matrix1[i][j] - matrix2[i][j], 2)
	eucDist = math.sqrt(differenceSum)
	return eucDist


# The parallel reading class to compute the orbit correlation distances
class correlDistanceComputer(multiprocessing.Process):
	def __init__(self, work_queue, result_queue, testMode):
		multiprocessing.Process.__init__(self)
		
		self.work_queue = work_queue
		self.result_queue = result_queue
		self.testMode = testMode
		self.kill_received = False
	
	def run(self):
		while not self.kill_received:
			# Get a task
			try:
				# matrixPair : 0,1 holds indexes; 2, 3 holds matrices; 4,5 holds sc_file_names
				matrixPair = self.work_queue.get_nowait()
				print("matrixPair", matrixPair)
				# distance = computeMatrixDist(matrixPair[2], matrixPair[3])
        # xxx here make an if statement using the type of distance
				if self.testMode == 1: # FDD (Facet Distribution Distance)
					distance = FDD_get_distance(matrixPair[4], matrixPair[5])
				elif self.testMode == 2:
					distance = SCD_get_distance(matrixPair[2], matrixPair[3])
				print("distance", distance)
				self.result_queue.put((matrixPair[0], matrixPair[1], distance))
				# self.result_queue.put((0, 0, distance)) # xxx
			except Queue.Empty:
				pass
			# except Exception as e:
			# 	print("Exception", e, e.message)


# The function to compute all the distances between the provided correlation matrices in parallel
def computeCorrelDist(corrMats, outputName, testMode):
	# Start the processes
	pair_queue = multiprocessing.Queue()
	result_queue = multiprocessing.Queue()
	processList = []
	
	for i in range(num_processes):
		computer = correlDistanceComputer(pair_queue, result_queue, testMode)
		computer.start()
		processList.append(computer)
	
	# Put the jobs to be consumed
	totalJobCount = len(corrMats) * (len(corrMats) - 1) / 2
	pairCount = 0
	print("corrMats", corrMats)
	print("corrMats.values()", corrMats.values())
	for i in range(len(corrMats) - 1):
		corrMat1 = corrMats.values()[i]
		scFile1 = corrMats.keys()[i]
		# corrMat1 = list(corrMats.values())[i] # ref:https://stackoverflow.com/questions/33674033/python-how-to-convert-a-dictionary-into-a-subscriptable-array
		
		for j in range(i+1, len(corrMats)):
			corrMat2 = corrMats.values()[j]
			scFile2 = corrMats.keys()[j]
			# corrMat2 = list(corrMats.values())[j] # ref:https://stackoverflow.com/questions/33674033/python-how-to-convert-a-dictionary-into-a-subscriptable-array
			
			pair_queue.put((i, j, corrMat1, corrMat2, scFile1, scFile2))
			pairCount += 1
		
			if pairCount % 1000 == 0:
				print('Jobs submitted: ', str(float(pairCount) / totalJobCount * 100), '%')
	
	
	# Process the results of computation
	distances = [[0] * len(corrMats) for i in range(len(corrMats))]
	
	computedCount = 0
	while computedCount < pairCount:
		try:
			results = result_queue.get_nowait()
			distances[results[0]][results[1]] = distances[results[1]][results[0]] = results[2]
			computedCount += 1
		except Queue.Empty:
			time.sleep(1)
		
		if computedCount % 1000 == 0:
			print('Jobs finished: ' , str(float(computedCount) / totalJobCount * 100), '%')
	
	for proc in processList:
		proc.terminate()
	
	# Save the results in the output file
	saveDistanceMatrix(distances, corrMats.keys(), outputName)

# -------------------

# Given a matrix, writes the matrix with the network names into the output file
def saveDistanceMatrix(matrix, networkNames, outputFile):
	fWrite = open(outputFile, 'w')
	
	# Write the names of the networks
	toWrite = '\t'
	for name in networkNames:
		toWrite += name + '\t'
	fWrite.write(toWrite.rstrip() + '\n')
	
	# Write the distances among networks
	for i in range(len(networkNames)):
		toWrite = networkNames[i] + '\t'
		for val in matrix[i]:
			toWrite += str(val) + '\t'
		fWrite.write(toWrite.rstrip() + '\n')
	
	fWrite.close()

# -------------------

# Computes the orbit correlation matrices for all the correlation matrices provided in allIndexes 
def getCorrelationMatrices(allIndexes, testMode):
	# Prepare the list of files to be processed
	# file_queue = multiprocessing.Queue()
	# result_queue = multiprocessing.Queue()
	
	# processList = []
	# for i in range(num_processes):
		# reader = MatrixReader(file_queue, result_queue, testMode)
		# reader.start()
		# processList.append(reader)
	
	# Put the jobs to be consumed
	# jobCount = len(allIndexes)
	# submitCount = 0
	
	# for index in allIndexes:
	# 	file_queue.put(index)
	# 	submitCount += 1
		
	# 	if submitCount % 100 == 0:
	# 		print 'Submitted correlation computation for: ' , str(float(submitCount) / jobCount * 100) , '%'

	# Process the results of computation
	correlMats = {}
	
	finishedCount = 0
	while finishedCount < len(allIndexes):
		try:
			# matrix = result_queue.get_nowait()
			# matrix = [allIndexes[finishedCount], numpy.array([[0,1,2],[0,1,2]])]
			matrix = [allIndexes[finishedCount], allIndexes[finishedCount] + '_signatures.sdv']
			correlMats[matrix[0]] = matrix[1]
			finishedCount += 1
		except Queue.Empty:
		# except Exception as e:
		# 	print("Exception", e)
			time.sleep(1)
		
		# if finishedCount % 100 == 0:
		# 	print 'Finished reading: ', str(float(finishedCount) / jobCount * 100) , '%'
	
	# for proc in processList:
	# 	proc.terminate()
	
	return correlMats

# -------------------

# ---------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------
args = sys.argv[1:]
print("args", args)

"""
	Main code starts here
"""
if __name__ == "__main__":
	# Process the program parameters
	ndumpFolder 	= sys.argv[1]
	if not ndumpFolder.endswith('/'):
		ndumpFolder += '/'

	if len(sys.argv) == 2:
		testMode = 1
	else:
		testMode = int(sys.argv[2])
		if testMode < 1 or testMode > 2:
			print('Unknown test mode! Current test mode is set to 1')
			testMode = 1
	
	if len(sys.argv) == 3:
		num_processes = 4
	else:
		num_processes = int(sys.argv[3])
	
	# Read the graphlet signatures or networks depending on the distance type
	allIndexes		= []	# The list of all processed network names

	directory = os.walk(ndumpFolder)
	
	for file in directory:
		path = file[0]
		
		for fileName in file[2]:
			#print fileName
			if fileName[-14:] == "signatures.sdv":
				stripName = fileName[:-15]
				indexName = path + '/' + stripName
				#print indexName
				
				allIndexes.append(indexName)
	print("step 0: located %s signature files"%(str(len(allIndexes))))
	
	
	# Compute the orbit correlation distance based on the set of orbits that we want to consider
	if testMode == 1:
		corrMats = getCorrelationMatrices(allIndexes, testMode)
		#printAverageCorrelMat(corrMats, ndumpFolder + 'average_correl_mat_' + str(testMode) + '.txt')
		print('Matrices ready! Computing the distances...')
		print("allIndexes", allIndexes)	
		print("corrMats", corrMats)
		computeCorrelDist(corrMats, ndumpFolder + 'FDD.txt', testMode)
	if testMode == 2:
		corrMats = getCorrelationMatrices(allIndexes, testMode)
		#printAverageCorrelMat(corrMats, ndumpFolder + 'average_correl_mat_' + str(testMode) + '.txt')
		print('Matrices ready! Computing the distances...')
		print("corrMats", corrMats)
		computeCorrelDist(corrMats, ndumpFolder + 'SCD.txt', testMode)
	# Compute the RGF Distance
	