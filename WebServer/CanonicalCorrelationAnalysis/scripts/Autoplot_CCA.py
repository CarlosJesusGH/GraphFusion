#!/usr/bin/env python

"""
	original code from Omer Nebil Yaveroglu
	modified by N. Malod-Dognin
"""

import sys
import os
import operator
import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.cm as cmx


"""
	Helper functions are defined here
"""

cdict = {'green': ((0.0, 0.0, 0.0), (0.7, 1.0, 1.0), (1.0, 1.0, 1.0)),
         'red': ((0.0, 1.0, 1.0), (0.3, 1.0, 1.0), (1.0, 0.0, 0.0)),
         'blue': ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0))}


def read_data(filename):
    matrix = []
    infile = open(filename, 'r')
    # column names, a.k.a variable names, are given on the first line
    header = [hh[1:-1] for hh in infile.readline().strip().split(',')[1:]]
    for line in infile.readlines():
        linesplit = line.strip().split(',')[1:]
        # bug fix for poorly formated matrix data
        row = []
        for elem in linesplit:
            val = 0.
            try:
                val = float(elem)
            except:
                val = float(elem[1:-1])
            row.append(val)
        matrix.append(row)
    infile.close()
    #for i in range(len(matrix)):
    #	if min(matrix[i]) == max(matrix[i]):
    #		print "Warning; ",header[i], "is constent !!!"
    matrix_ar = np.array(matrix)
    return [header, matrix_ar]


def readCor(corFile, index):
    variateDict = {}

    fRead = open(corFile, 'r')

    title = fRead.readline()
    for line in fRead:
        splitted = line.strip().split(',')

        attrName = splitted[0].strip('\"')
        # if attrName.startswith('sig_'):
        #	attrName = attrName.strip('sig_')

        corVal = float(splitted[index])

        variateDict[attrName] = corVal

    fRead.close()

    sortedVariates = sorted(variateDict.iteritems(), key=operator.itemgetter(1), reverse=True)

    return sortedVariates


# Plot the highest ranking attributes
def plotAttributes(econVar, topoVar, cca_val, pvalue, outputFile):
    fig = plt.figure()
    fig.suptitle("CCA = %.3f, p-value = %s" % (cca_val, '{:.2e}'.format(pvalue)), fontsize=14)
    ax_left = fig.add_axes((0.05, 0.05, 0.43, 0.9))
    ax_right = fig.add_axes((0.52, 0.05, 0.43, 0.9))
    ax_heat = fig.add_axes((0.48, 0.05, 0.04, 0.9))

    # Define the colormap and Add the colorbar at the center of the image
    gradient = np.linspace(-1, 1, 256)
    gradient = np.vstack((gradient, gradient))
    gradient = gradient.transpose()
    my_cmap = colors.LinearSegmentedColormap('GreenRed', cdict)
    cNorm = colors.Normalize(vmin=-1, vmax=1)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=my_cmap)
    ax_heat.imshow(gradient, aspect='auto', cmap=my_cmap)

    ax_heat.get_xaxis().set_visible(False)
    ax_heat.get_yaxis().set_visible(False)
    ax_heat.axis('off')

    # ax_heat.patch.set_facecolor('black')
    xlimits = ax_heat.get_xlim()
    ax_heat.plot(xlimits, [128, 128], color='white', linewidth=3)
    ax_heat.set_ylim(0, 256)

    # Plot the lines for left axis
    ax_left.get_xaxis().set_visible(False)
    ax_left.get_yaxis().set_visible(False)
    ax_left.axis('off')
    ax_left.patch.set_facecolor('white')

    for i in range(len(econVar)):
        xcoords = 0.1
        ycoords = 0.95 - (i * (2.0 / len(econVar)))
        ax_left.text(xcoords, ycoords, econVar[i][0].replace('per', ' per '), color='black')


        #if i < 5:
        #	multind = 7-i
        #else:
        #	multind = i
        multind = i
        #if i < 5:
        #	multind = i+5
        #else:
        #	multind = i

        #print i, multind


        ax_left.plot([0.5, 0.5 + (multind * 0.025)], [ycoords + 0.025, ycoords + 0.025], linewidth=1,
                     color=scalarMap.to_rgba(econVar[i][1]))
        ax_left.plot([0.5 + (multind * 0.025), 0.5 + (multind * 0.025)], [ycoords + 0.025, econVar[i][1]], linewidth=1,
                     color=scalarMap.to_rgba(econVar[i][1]))
        ax_left.plot([0.5 + (multind * 0.025), 1], [econVar[i][1], econVar[i][1]], linewidth=1,
                     color=scalarMap.to_rgba(econVar[i][1]))

    ax_left.set_xlim(0, 1)
    ax_left.set_ylim(-1, 1)

    # Plot the lines for right axis
    ax_right.get_xaxis().set_visible(False)
    ax_right.get_yaxis().set_visible(False)
    ax_right.patch.set_facecolor('white')
    ax_right.axis('off')

    ax_right.set_xlim(0, 1)
    ax_right.set_ylim(-1, 1)

    for i in range(len(topoVar)):
        xcoords = 0.9
        ycoords = 0.95 - (i * (2.0 / len(topoVar)))
        ax_right.text(xcoords, ycoords, topoVar[i][0].replace('per', ' per '), color='black')

        #if i < 10:
        #	multind = 10 - i
        #else:
        #	multind = 20 - i
        #
        #if i < 6:
        #	multind = i
        #elif i < 11:
        #	multind = 15 - i
        #else:
        #	multind = 20 - i
        #print i , multind
        multind = i
        #print 0.0, topoVar[i][1], 0.15 + (multind * 0.025), topoVar[i][1]
        ax_right.plot([0.0, 0.15 + (multind * 0.025)], [topoVar[i][1], topoVar[i][1]], linewidth=1.5,
                      color=scalarMap.to_rgba(topoVar[i][1]))
        ax_right.plot([0.15 + (multind * 0.025), 0.15 + (multind * 0.025)], [topoVar[i][1], ycoords + 0.02],
                      linewidth=1.5, color=scalarMap.to_rgba(topoVar[i][1]))
        ax_right.plot([0.15 + (multind * 0.025), 0.85], [ycoords + 0.02, ycoords + 0.02], linewidth=1.5,
                      color=scalarMap.to_rgba(topoVar[i][1]))
    # - ((i%2) * 0.2)
    fig.savefig(outputFile, format='png', facecolor='white')

# fig.savefig('test.pdf', format = 'pdf')


"""
	Main code starts here
"""
if __name__ == "__main__":
    xname = sys.argv[1]  #name of X variable
    yname = sys.argv[2]  #name of Y variables
    directory = sys.argv[3]  #working directory
    prefix = sys.argv[4]  #data prefix
    tokeep = int(sys.argv[5])  # maximum number of considered X or Y variables (ps, bug if set > 14)

    xloadingname = directory + "/" + prefix + "_X-loadings.csv"
    yloadingname = directory + "/" + prefix + "_Y-loadings.csv"
    yxcancorname = directory + "/" + prefix + "_XY_canonical-correlations.csv"

    variates, cancors = read_data(yxcancorname)
    nb_variates = len(cancors)
    nb_signif_variates = 0
    for v in range(nb_variates):
        if cancors[v][1] <= 0.05:
            nb_signif_variates += 1
    #print cancors
    for i in range(1, nb_signif_variates + 1):
        ccaval = cancors[i - 1][0]
        pval = cancors[i - 1][1]
        xVar = readCor(xloadingname, i)
        yVar = readCor(yloadingname, i)
        #keeping only the highest X loadings
        x_sorter = {}
        for val in xVar:
            xname = val[0]
            xvalue = abs(val[1])
            if xvalue not in x_sorter:
                x_sorter[xvalue] = []
            x_sorter[xvalue].append(xname)
        xkeys = x_sorter.keys()
        xkeys.sort()
        xkeys.reverse()
        sorted_xnames = []
        for key in xkeys:
            for item in x_sorter[key]:
                sorted_xnames.append(item)
        xToKeep = sorted_xnames[:tokeep]
        #keeping only the highest X loadings
        y_sorter = {}
        for val in yVar:
            yname = val[0]
            yvalue = abs(val[1])
            if yvalue not in y_sorter:
                y_sorter[yvalue] = []
            y_sorter[yvalue].append(yname)
        ykeys = y_sorter.keys()
        ykeys.sort()
        ykeys.reverse()
        sorted_ynames = []
        for key in ykeys:
            for item in y_sorter[key]:
                sorted_ynames.append(item)
        yToKeep = sorted_ynames[:tokeep]
        #preparing X data for plotting
        xToPlot = []
        for var in xVar:
            if var[0] in xToKeep:
                xToPlot.append(var)
        #preparing Y data for plotting
        yToPlot = []
        for var in yVar:
            if var[0] in yToKeep:
                yToPlot.append(var)
        #calling the plot function
        outputFile = directory + "/" + prefix + "_cancor_" + str(i) + ".png"
        plotAttributes(xToPlot, yToPlot, ccaval, pval, outputFile)

