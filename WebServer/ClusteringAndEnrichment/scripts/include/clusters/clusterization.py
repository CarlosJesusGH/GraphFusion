import numpy as np
# import h5py
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
# Load entity list. The [:,0] is to get the first column of the dataframe, which is the list of entities. Load it with header=None to avoid the first row being interpreted as the header.
entities = pd.read_csv(op_dir + "/" + entitylist_filename, header=None).iloc[:,0].values

# print("entities", entities)
# entities = np.loadtxt(open(op_dir + "/" + "icell_genelist.csv", "rb"), delimiter="\t", skiprows=0)
# print("entities", entities)
# clusters = extractClusters(factor)
# compute clusters using psb script in DataFusion/scripts/include/psb/scripts/ResultsAnalysis/enrichementAnalysis.py
clusters = extractClusters(entities, factor)

print("type(clusters)", type(clusters))
print("type(clusters[0])", type(clusters[0]))
print("type(clusters[0][0])", type(clusters[0][0]))
# print("clusters", clusters)

np.save(op_dir + "/" + "clusters.npy", clusters)
# print("clusters", clusters)
# np.savetxt(op_dir + "/" + "clusters.csv", clusters, delimiter="\t")
# import pickle
# pickle.dump(clusters, open(op_dir + "/" + "clusters.csv", "wb"))

# sort clusters by size
sorted_clusters = sorted(clusters, key=len, reverse=True)
# print("sorted_clusters", sorted_clusters)



import csv
with open(op_dir + "/" + "clusters.csv", "w", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerows(sorted_clusters)

# with open(op_dir + "/" + "clusters.csv", "w") as f:
#     for cluster in clusters:
#         f.write("\t".join(cluster))

cluster_lens = [len(cluster) for cluster in clusters]
plt.bar(range(len(cluster_lens)), sorted(cluster_lens, reverse=True))

# set axis labels and title
plt.xlabel("Clusters")
plt.ylabel("Number of entities")
plt.title("Histogram - Number of entities per cluster")

plt.savefig(op_dir + "/" + "clusters_from_factor.svg")