"""
	The script reads an ndump2 file and does the following:
	
	1) Computes the GCM of the specified type
	2) Outputs the GCM in csv format
	3) Draws the GCM
	
	The drawing can be performed by clustering for the identification
	of orbit clusters automatically or based on a given orbit order
	
	Run as:
		python computeGCM.py <ndump_file> <gcm_type> <orbit_order_mode>
		
		<gcm_type>:
			11 - uses all non-redundant 2-to-5 node graphlet orbits
			15 - uses all 2-to-4 node graphlet orbits
			73 - uses all 2-to-5 node graphlet orbits
		
		<orbit_order_mode>:
			0 - sorts the orbits and draws accordingly
			1 - automatically orders the graphlet orbits
			<orbit_order_file> - a file containing a particular order of orbits to draw
				If providing an orbit_order file, the orbits should be separated with comma (,)
				without spaces, should be written in a single line, and all orbits should match
				the corresponding gcm_type
	
	Implemented by:
		Omer Nebil Yaveroglu
		Original version implemented on	: 25.05.2012 - 12:42
		Clean Version implemented on 	: 06.06.2015 - 12:11
"""

import sys
import csv
import os
import numpy

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from scipy import stats

"""
	Functions
"""
# Read the signatures from ndump2 files
def readSignatures(file, gcmType):
    # Identify the orbits to consider
    if gcmType == '11':
        orbitList = [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11]
    elif gcmType == '15':
        orbitList = range(15)
    elif gcmType == '73':
        orbitList = range(73)

    # Read the ndump2 file for these orbits
    signList = []

    fRead = open(file, 'r')

    for line in fRead:
        gdv = [float(val) for val in line.strip().split(' ')[-73:]]
        signList.append([gdv[orbit] for orbit in orbitList])

    fRead.close()

    return (signList, orbitList)


# Compute the correlations among the orbits while avoiding isnan values
def computeCorrelations(signatureList):
    length = len(signatureList[0])

    # To avoid isnan correlations, add a signature [1, 1, ..., 1]
    signs = signatureList[:]  # Create a copy of the signatureList
    signs.append([1] * length)  # Add the dummy signature as a slight noise

    # Compute the Spearman's correlations among the graphlet degrees of different orbit pairs
    rankList = []
    for orbit in range(length):
        rankList.append(stats.mstats.rankdata([gd[orbit] for gd in signs]))

    correlMat = numpy.corrcoef(rankList, rowvar=1)

    return correlMat


# The function to identify the correct orbit order to draw the heatmap
def identifyOrbitOrder(orbitList, correlMat, gcmType, orbitOrder):
    orderedOrbits = None

    if orbitOrder == '0':
        orderedOrbits = orbitList
    elif orbitOrder == '1':
        # Do the automatic clustering

        # Transform correlations into distance matrix for linkage function
        correlDists = []
        for corlist in correlMat:
            correlDists.append([(1 - val) for val in corlist])

        # Compute the linkage
        Y = sch.linkage(correlDists, method='average')
        treeOrder = sch.to_tree(Y).pre_order()

        if gcmType == '11':
            orderedOrbits = []
            for val in treeOrder:
                if val >= 3:
                    orderedOrbits.append(val + 1)
                else:
                    orderedOrbits.append(val)
        else:
            orderedOrbits = treeOrder

    else:
        # Read the orbit list file for getting the requested orbit order
        fRead = open(orbitOrder, 'r')
        orderedOrbits = [int(val) for val in fRead.readline().strip().split(',')]

        if len(orderedOrbits) <> len(orbitList):
            print 'ERROR: Check orbit list file -- orbit lists do not match!'
            exit(0)

        for orbit in orderedOrbits:
            if orbit not in orbitList:
                print 'ERROR: Check orbit list file -- unfound orbit: {0}'.format(orbit)
                exit(0)

        for orbit in orbitList:
            if orbit not in orderedOrbits:
                print 'ERROR: Check orbit list file -- Missing orbit: {0}'.format(orbit)
                exit(0)

        fRead.close()

    return orderedOrbits


# Redraw the heatmap based on the new clusters
def drawHeatmap(correlMat, orbitList, gcmType, orbitOrder, outputName):
    # Identify the orbit order to draw
    sortedOrbits = identifyOrbitOrder(orbitList, correlMat, gcmType, orbitOrder)

    # Reorder the correlation matrix
    if gcmType == '11':
        reorderOrbits = []
        for val in sortedOrbits:
            if val > 3:
                reorderOrbits.append(val - 1)
            else:
                reorderOrbits.append(val)
    else:
        reorderOrbits = sortedOrbits

    correlMat2 = numpy.matrix(correlMat)
    correlMat2 = correlMat2[reorderOrbits, :]
    correlMat2 = correlMat2[:, reorderOrbits]

    # Plot the correlation matrix
    fig = plt.figure(figsize=(20, 20))
    axmatrix = fig.add_axes([0.07, 0.04, 0.80, 0.88])

    im = axmatrix.matshow(correlMat2, aspect='auto', cmap=plt.cm.jet, vmin=-1, vmax=1)
    axmatrix.set_xticks(range(len(sortedOrbits)))
    axmatrix.set_yticks(range(len(sortedOrbits)))
    axmatrix.set_xticklabels(sortedOrbits, rotation=90)
    axmatrix.set_yticklabels(sortedOrbits)

    # Plot colorbar
    axcolor = fig.add_axes([0.9, 0.04, 0.02, 0.88])
    plt.colorbar(im, cax=axcolor)
    print "outputname is ", outputName
    fig.savefig(outputName, format='svg')


# The function to do the checks for script parameters
def inputErrorChecks(ndump2File, gcmType, orbitOrder):
    # Check graphlet signature file
    if not ndump2File.endswith('ndump2'):
        print 'The graphlet signatures should be provided in ndump2 format!'
        exit(0)
    elif not os.path.isfile(ndump2File):
        print 'Graphlet signatures file could not be found!'
        exit(0)

    # Check gcmType parameter
    if gcmType not in ['11', '15', '73']:
        print 'Unknown GCM type: {0}'.format(gcmType)
        exit(0)

    # Check orbitOrder parameter
    if not (orbitOrder == '0' or orbitOrder == '1' or os.path.isfile(orbitOrder)):
        print 'Unknown Orbit Order Type or File Not Found: {0}'.format(orbitOrder)
        exit(0)


# The function to output the graphlet correlation matrix
def writeGCM(correlMat, orbitList, csvFile):
    with open(csvFile, 'w') as outputFile:
        writer = csv.writer(outputFile)

        # Write the titles
        writer.writerow([''] + orbitList)

        # Write the orbit correlations
        for i in range(len(orbitList)):
            writer.writerow([orbitList[i]] + list(correlMat[i]))


"""
	The main function starts here
"""

if __name__ == '__main__':
    ndump2File = sys.argv[1]
    gcmType = sys.argv[2]
    orbitOrder = sys.argv[3]
    # print("log - ndump2File", ndump2File, "gcmType", gcmType, "orbitOrder", orbitOrder)

    inputErrorChecks(ndump2File, gcmType, orbitOrder)

    # Read the graphlet signatures
    (signList, orbitList) = readSignatures(ndump2File, gcmType)

    # Compute the correlation matrix
    correlMat = computeCorrelations(signList)

    # Output the correlation matrix
    outputFile = '{0}_gcm{1}.csv'.format(ndump2File.rsplit('.', 1)[0], gcmType)
    writeGCM(correlMat, orbitList, outputFile)

    # Draw the correlation matrix as requested
    drawFile = '{0}_gcm{1}.svg'.format(ndump2File.rsplit('.', 1)[0], gcmType)
    drawHeatmap(correlMat, orbitList, gcmType, orbitOrder, drawFile)
