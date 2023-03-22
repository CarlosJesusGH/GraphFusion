# -*- coding: utf-8 -*-

import os
import sys
import scipy.stats as ss
import numpy.linalg as nl
import numpy as np
import matplotlib.pyplot as plt
import math


# A class for performing Canonical Correlation Analysis
class Class_CCA:
    # Load data matrix from file. Rows = samples, columns = values of variable.
    # - first row contain variable names
    # - first variable (1st column) sould be sample name, and is ignored
    def read_data(self, filename, use_log=False):
        print filename
        matrix = []
        infile = open(filename, 'r')
        # column names, a.k.a variable names, are given on the first line
        header = infile.readline().strip().split(',')[1:]
        for line in infile.readlines():
            linesplit = line.strip().split(',')[1:]
            # bug fix for poorly formated matrix data
            row = []
            for elem in linesplit:
                val = 0.
                try:
                    val = float(elem)
                except:
                    print elem
                    val = float(elem[1:-1])
                row.append(val)
            matrix.append(row)
        infile.close()
        # for i in range(len(matrix)):
        # if min(matrix[i]) == max(matrix[i]):
        # print "Warning; ",header[i], "is constent !!!"
        if use_log == True:
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    matrix[i][j] = math.log(matrix[i][j] + 1.)
        print filename, ": ", len(header), " variables over ", len(matrix), " samples..."
        matrix_ar = np.array(matrix)
        return [header, matrix_ar]

    # Write a matrix in a file that can be loaded easily by matlab
    def write_R_matrix(self, filename, data):
        ofile = open(filename, 'w')
        dimX = len(data)
        dimY = len(data[0])
        for x in range(dimX):
            ofile.write("%s" % (data[x][0]))
            for y in range(1, dimY):
                ofile.write("\t%s" % (data[x][y]))
            ofile.write("\n")
        ofile.close()

    # load the CCA output from matlab run
    def load_R_output(self, output_dir, prefix):

        fprefix = output_dir + "/" + prefix

        # r = the canonical correlations chi
        ifile = open(fprefix + "__XY-chi.csv")
        chi = []
        ifile.readline()
        for line in ifile.readlines():
            chi.append(float(line.strip().split(',')[1]))
        ifile.close()

        # A = the canonical weights of X
        ifile = open(fprefix + "__X-weights.csv")
        A = []
        ifile.readline()
        for line in ifile.readlines():
            lnspt = line.strip().split(',')[1:]
            A.append([float(i) for i in lnspt])
        ifile.close()

        # B = the canonical weights of Y
        ifile = open(fprefix + "__Y-weights.csv")
        B = []
        ifile.readline()
        for line in ifile.readlines():
            lnspt = line.strip().split(',')[1:]
            B.append([float(i) for i in lnspt])
        ifile.close()

        Ar = np.array(A)
        Br = np.array(B)

        return [Ar, Br, chi]

    # check that the largest discrepancy between correlations is less that 1E-3
    def validate_cancor(self, r, r2):
        max_err = 0.;
        for i in range(len(r)):
            err = abs(r[i] - r2[i][0])
            if err > max_err:
                max_err = err
        if max_err >= 0.001:
            print "-- Warning: Canonical correlation mismatch"

    # compute loadings from scratch
    def calc_loadings(self, X, X_t):
        dimX = len(X[0])
        dimN = len(X_t[0])
        loadingsX = []
        X_o = [[X[sample][dim] for sample in range(len(X))] for dim in range(dimX)]
        X_n = [[X_t[sample][dim] for sample in range(len(X))] for dim in range(dimN)]
        for dim_o in range(dimX):
            load_o = []
            for dim_n in range(dimN):
                pcc = ss.pearsonr(X_o[dim_o], X_n[dim_n])
                mypcc = pcc[0]
                if math.isnan(mypcc):
                    mypcc = 0.0
                load_o.append(mypcc)
            loadingsX.append(load_o)
        return loadingsX

    # Output rsquared
    def output_can_cor(self, filename, cancor):
        ofile = open(filename, 'w')
        ofile.write("\"variate\",\"chi\"\n")
        for i in range(len(cancor)):
            ofile.write("\"V%i\",%s\n" % (i + 1, str(cancor[i])))
        ofile.close()

    #Output PCCs
    def output_can_cor2(self, filename, cancor):
        ofile = open(filename, 'w')
        ofile.write("\"variate\",\"pcc\",\"p-val\"\n")
        for i in range(len(cancor)):
            ofile.write("\"V%i\",%s,%s\n" % (i + 1, str(cancor[i][0]), str(cancor[i][1])))
        ofile.close()

    #output the canonical weights
    def output_weights(self, filename, header, weights):
        ofile = open(filename, 'w')
        dim_ori = len(header)
        dim_new = len(weights[0])
        #print header
        ofile.write("\"\"")
        for i in range(dim_new):
            ofile.write(",\"V%i\"" % (i + 1))
        ofile.write("\n")
        #print weights for each original variable
        for dim_o in range(dim_ori):
            ofile.write("\"%s\"" % (header[dim_o]))
            for dim_n in range(dim_new):
                ofile.write(",%s" % (str(weights[dim_o][dim_n])))
            ofile.write("\n")
        ofile.close()

    #output loadings
    def output_loadings(self, filename, header, loading):
        ofile = open(filename, 'w')
        dim_ori = len(header)
        dim_new = len(loading[0])
        #print header
        ofile.write("\"\"")
        for i in range(dim_new):
            ofile.write(",\"V%i\"" % (i + 1))
        ofile.write("\n")
        #print weights for each original variable
        for dim_o in range(dim_ori):
            ofile.write("%s" % (header[dim_o]))
            for dim_n in range(dim_new):
                ofile.write(",%s" % (str(loading[dim_o][dim_n])))
            ofile.write("\n")
        ofile.close()

    #compute association scores, e.g., correlations between X and X_pred
    # -- from using first to all canonical variates
    def calc_association_scores_all(self, X, mat_pred_X, header, dimX, dimN):
        #dimX = len(X[0])
        Pred_ass = [[0. for k in range(dimX)] for i in range(dimN)]
        Pred_pval = [[0. for k in range(dimX)] for i in range(dimN)]
        X_o = [[X[sample][dim] for sample in range(len(X))] for dim in range(dimX)]
        avg_pcc = []
        for i in range(dimN):
            X_t = np.array(mat_pred_X[i])
            X_p = [[X_t[sample][dim] for sample in range(len(X))] for dim in range(dimX)]
            apcc = 0.
            for dim in range(dimX):
                obs = np.array(X_o[dim])
                pred = np.array(X_p[dim])
                pcc = ss.pearsonr(obs, pred)
                #print X_o[dim]
                #print X_p[dim]
                pcc_val = pcc[0]
                if math.isnan(pcc_val):
                    pcc_val = 0.
                Pred_ass[i][dim] = pcc_val
                Pred_pval[i][dim] = pcc[1]
                apcc += pcc_val
            apcc /= float(dimX)
            avg_pcc.append(apcc)

        return [avg_pcc, Pred_ass, Pred_pval]

    #perform CCA using matlab
    def Analyze_All(self, data_fnameX, data_fnameY, output_dir, prefix, use_log):

        #load input data
        headerX, X = self.read_data(data_fnameX + ".csv")
        headerY, Y = self.read_data(data_fnameY + ".csv", use_log)
        dimX = len(headerX)
        dimY = len(headerY)
        nb_samples = len(X)

        #prepare data for R/matlab call
        fnamex = output_dir + "/" + prefix + "_X.csv"
        fnamey = output_dir + "/" + prefix + "_Y.csv"
        fprefix = output_dir + "/" + prefix
        self.write_R_matrix(fnamex, X)
        self.write_R_matrix(fnamey, Y)
        cmd = "Rscript %s %s %s %s" % (my_CCA_R_script_filepath, fnamex, fnamey, fprefix)
        print "Calling R to perform CCA..."
        os.system(cmd)
        print "Loading R output..."
        A, B, chi = self.load_R_output(output_dir, prefix)
        dimN = len(chi)
        print "--> ", dimN, " canonical variates"

        #computing canonical correlation from scratch, by using Pearson's correlation between transformed samples
        # - this allows us to get p-values
        print "Re-computing canonical correlations..."
        r = []
        U = np.dot(X, A)
        V = np.dot(Y, B)
        X_v = np.transpose(U)
        Y_v = np.transpose(V)
        for variate in range(dimN):
            pcc = ss.pearsonr(X_v[variate], Y_v[variate])
            r.append([pcc[0], pcc[1]])

        # Sanity check: Validating canonical correlations
        #self.validate_cancor(r, r_2)
        print "Outputing correlations and weights..."
        self.output_can_cor(output_dir + "/" + prefix + "_XY_chi.csv", chi)
        self.output_can_cor2(output_dir + "/" + prefix + "_XY_canonical-correlations.csv", r)
        self.output_weights(output_dir + "/" + prefix + "_X-weights.csv", headerX, A)
        self.output_weights(output_dir + "/" + prefix + "_Y-weights.csv", headerY, B)

        #computing loadings from scratch, by using Pearson's correlation between original variable and canonical variates

        print "Computing loadings..."
        loadingsX = self.calc_loadings(X, U)
        loadingsY = self.calc_loadings(Y, V)
        self.output_loadings(output_dir + "/" + prefix + "_X-loadings.csv", headerX, loadingsX)
        self.output_loadings(output_dir + "/" + prefix + "_Y-loadings.csv", headerY, loadingsY)


if __name__ == '__main__':
    data_fnameX = sys.argv[1]  # filename, without .csv extention
    data_fnameY = sys.argv[2]  # filename, without .csv extention
    output_dir = sys.argv[3]  # output_directory
    prefix = sys.argv[4]  # output_prefix
    use_log = sys.argv[5]  # use log: 0 = false, 1 = true
    my_CCA_R_script_filepath = sys.argv[6]
    uselogbool = False
    if use_log == '1':
        uselogbool = True
    myCCA = Class_CCA()
    myCCA.Analyze_All(data_fnameX, data_fnameY, output_dir, prefix, uselogbool)