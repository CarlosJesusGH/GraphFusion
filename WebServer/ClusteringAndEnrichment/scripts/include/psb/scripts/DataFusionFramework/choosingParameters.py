import pandas as pd
import numpy as np

import sys
sys.path.append('../scripts/')
from utils import getHardClusters


def createConnectivityMatrix(clusters, k, col):
    """
    Create the connectivity matrix
    
    Parameters
    ----------
    clusters: DataFrame
        Each column contain the cluster indicators for the elements in the index
    k: integer
        Indicates the number of clusters
    col: string
        Indicates the column from which the connectivy matrix must be computed
        
    Return
    ------
    Returns the created connectivity matrix in a DataFrame.
    
    """

    
    connectivityMatrix = pd.DataFrame(np.zeros((clusters.shape[0], clusters.shape[0])), \
                                      index=clusters.index, columns=clusters.index)
    for nC in range(k):
        nodes = clusters[clusters[col] == nC].index
        cMTmp = pd.DataFrame(np.ones((nodes.shape[0], nodes.shape[0])), index=nodes, columns=nodes)
        connectivityMatrix.update(cMTmp)

    return connectivityMatrix.values

def copeheneticCorreletionCoef(matrix):
    """
    Computed the copehenetic correlation coefficient from a matrix
    
    Parameters
    ----------
    matrix: numpy
        contains the matrix with the clusters (consensus matrix)
        
    Return
    ------
    Returns the correlaction coefficient.
    
    """
    
    n = matrix.shape[0]
    coef = 0
    for row in matrix:
        for item in row:
            coef += 4*(item - (1/2))**2
    return 1/n**2 * coef

def computeDispersionCoefficient(clusterElements, alphas = [0.6], k1s = [3,5], k2s = [80,100,60,120], k3s = [80,60,40], R=10, path='../Data/Results/', savePath='../Data/Results/', verbose=True):
    """
    Compute the dispersion coefficient for each parameter from the cluster indicatiors factors of a GNMTF factorization for different parametrizations and runs. It saves the clusters of the different runs in a same file and the consensus matrix computed.
    
    Parameters
    ----------
    clusterElements: list of lists
        Indicates the names of the elements of the different 
    alphas: list
        Indicated the values for the parameter alpha. By default [0.6] 
    k1s: list
        Indicated the values for the parameter k1. By default [3,5] 
    k2s: list
        Indicated the values for the parameter k2. By default [80,100,60,120]
    k3s: list
        Indicated the values for the parameter k3. By default[80,60,20]
    R: list
        Indicated the number of runs. By default 10
    path: string
        Indicated the path where the factor matrices are stored. By default'../Data/Results/'       
    savePath: string
        Indicated the path where the results must be saved. By default'../Data/Results/'
        
    verbose: boolean
        Indicates whether information of the dataset have to be printed. By default True

        
    Return
    ------
    Returns the dispersion coefficient for each parameter in a DataFrame
    
    """

    
    res= []
    for alpha in alphas:
        for k1 in k1s:
            for k2 in k2s:
                for k3 in k3s:

                    if verbose: print('alpha={}, k1={}, k2={}, k3={}'.format(alpha, k1, k2, k3))

                    #Initializate the clusters and consensus matrices
                    clustersG1 = pd.DataFrame(index=clusterElements[0])
                    clustersG2 = pd.DataFrame(index=clusterElements[1])
                    clustersG3 = pd.DataFrame(index=clusterElements[2])

                    consensusMatrixG1 = np.zeros((len(clusterElements[0]), len(clusterElements[0])))
                    consensusMatrixG2 = np.zeros((len(clusterElements[1]), len(clusterElements[1])))
                    consensusMatrixG3 = np.zeros((len(clusterElements[2]), len(clusterElements[2])))

                    #Compute the connectivity and consensus matrices form the G factors
                    for r in range(R):
                        if verbose:  print('Run: ', r)
                        G1 = np.load(path+'/{}_{}_{}_{}/G1_{}.npy'.format(str(alpha), str(k1), str(k2), str(k3), str(r)))
                        G2 = np.load(path+'/{}_{}_{}_{}/G2_{}.npy'.format(str(alpha), str(k1), str(k2), str(k3), str(r)))
                        G3 = np.load(path+'/{}_{}_{}_{}/G3_{}.npy'.format(str(alpha), str(k1), str(k2), str(k3), str(r)))

                        clustersG1.insert(clustersG1.shape[1], str(r), getHardClusters(G1))
                        clustersG2.insert(clustersG2.shape[1], str(r), getHardClusters(G2))
                        clustersG3.insert(clustersG3.shape[1], str(r), getHardClusters(G3))

                        if verbose:  print(' CM-G1 Completed')
                        consensusMatrixG1 += createConnectivityMatrix(clustersG1, k1, str(r))
                        if verbose:  print(' CM-G2 Completed')
                        consensusMatrixG2 += createConnectivityMatrix(clustersG2, k2, str(r))
                        if verbose:  print(' CM-G3 Completed')
                        consensusMatrixG3 += createConnectivityMatrix(clustersG3, k3, str(r))

                    #Save the clusters
                    clustersG1.to_csv(savePath+'/{}_{}_{}_{}/G1_clusters.csv'.format(str(alpha), str(k1), str(k2), str(k3), str(r)))
                    clustersG2.to_csv(savePath+'/{}_{}_{}_{}/G2_clusters.csv'.format(str(alpha), str(k1), str(k2), str(k3), str(r)))
                    clustersG3.to_csv(savePath+'/{}_{}_{}_{}/G3_clusters.csv'.format(str(alpha), str(k1), str(k2), str(k3), str(r)))

                    #Normalize the consensus matrices
                    consensusMatrixG1 = consensusMatrixG1 / R
                    consensusMatrixG2 = consensusMatrixG2 / R
                    consensusMatrixG3 = consensusMatrixG3 / R

                    #Saving the consensus Matrices
                    np.save(savePath+'/{}_{}_{}_{}/G1_ConsensusMatrix.npy'.format(str(alpha), str(k1), str(k2), str(k3), str(r)), consensusMatrixG1)
                    np.save(savePath+'/{}_{}_{}_{}/G2_ConsensusMatrix.npy'.format(str(alpha), str(k1), str(k2), str(k3), str(r)), consensusMatrixG2)
                    np.save(savePath+'/{}_{}_{}_{}/G3_ConsensusMatrix.npy'.format(str(alpha), str(k1), str(k2), str(k3), str(r)), consensusMatrixG3)

                    #Compute Dispersion Coefficient
                    dispersionCoefG1 = copeheneticCorreletionCoef(consensusMatrixG1)
                    dispersionCoefG2 = copeheneticCorreletionCoef(consensusMatrixG2)
                    dispersionCoefG3 = copeheneticCorreletionCoef(consensusMatrixG3)

                    res.append([alpha, k1, k2, k3, dispersionCoefG1, dispersionCoefG2, dispersionCoefG3])

    #Create a dataframe with the results and save it
    dfRes = pd.DataFrame(res, columns = ['Alpha', 'k1', 'k2', 'k3', 'DispCoef-k1', 'DispCoef-k2', 'DispCoef-k3'])
    display(dfRes)
    dfRes.to_csv(savePath+'/DispCoef_all.csv'.format(str(alpha), str(k1), str(k2), str(k3), str(r)))