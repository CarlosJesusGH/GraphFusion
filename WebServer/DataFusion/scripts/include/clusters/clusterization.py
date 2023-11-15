import numpy as np
import h5py
import pandas as pd
import os
import sys

sys.path.append(os.path.join(sys.path[0], '../psb/scripts/')); # print("sys.path", sys.path)
from ResultsAnalysis.enrichementAnalysis import *

# ---------------------------------------------------------------

def extractClusters_noEntityList(G):
    """
    Extract clusters from the clusters indicators using hard clustering
    
    Parameters
    ----------
    names: list
        Contains the name of the entities (i.e., genes or drugs)
    fileName: string
        Indicates the file containing the cluster in

    Return
    ------
    Return the clusters in a list of lists where every list is a cluster.
    
    """

    # G = np.load(fileName)

    # dfClusters = pd.DataFrame(getHardClusters(G), index=names).reset_index() 
    dfClusters = pd.DataFrame(getHardClusters(G)).reset_index()
    dfClusters.columns = ['Entity', 'Cluster']
    
    clusters = [list(dfClusters[dfClusters['Cluster'] == cluster]['Entity'].values) for cluster in dfClusters.sort_values('Cluster')['Cluster'].unique()]
    
    return clusters

# def getHardClusters(G):
#     """
#     Compute hard clustering from a G factor comming from a NMTF factorization
    
#     Parameters
#     ----------
#     G: numpy array
#         Contains G factor (cluster indicator) of a NMTF factorization
        
#     Return
#     ------
#     Returns the cluster indicator of each entry in a list.
    
#     """

#     return [np.argmax(G[i]) for i in range(G.shape[0])]




# ---------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------

args = sys.argv[1:]
op_dir, fact_name, entitylist_filename = args[0], args[1], args[2]

print("op_dir", op_dir)
print("fact_name", fact_name)

import matplotlib.pyplot as plt

# with h5py.File(op_dir + "/" + fact_name, "r") as f:
#     factor = np.array(f.get('dataset'))
factor = np.loadtxt(open(op_dir + "/" + fact_name, "rb"), delimiter="\t", skiprows=0)
# print("factor: ", factor)
print("factor.shape", factor.shape)

# entities = range(factor.shape[0])
entities = pd.read_csv(op_dir + "/" + entitylist_filename, header=None).iloc[:,0].values
# entities = np.loadtxt(open(op_dir + "/" + "icell_genelist.csv", "rb"), delimiter="\t", skiprows=0)
# print("entities", entities)
# clusters = extractClusters(factor)
clusters = extractClusters(entities, factor)

print("type(clusters[0][0])", type(clusters[0][0]))
# print("clusters", clusters)

np.save(op_dir + "/" + "clusters.npy", clusters)

cluster_lens = [len(cluster) for cluster in clusters]
plt.bar(range(len(cluster_lens)), sorted(cluster_lens, reverse=True))

plt.savefig(op_dir + "/" + "clusters_from_factor.svg")