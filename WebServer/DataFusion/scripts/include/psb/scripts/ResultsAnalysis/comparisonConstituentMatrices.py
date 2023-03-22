import networkx as nx
import pandas as pd
import numpy as np

def convertEdgeList(df):
    """
    Convert the edge list to a list of edges
    
    Parameters
    ----------
    df : pandas DataFrame
        Contains the edge list.
        
    Return
    ------
    Returns the list of edges
    
    """
    
    col1, col2 = df.columns[0], df.columns[1]

    d = []
    for ind, item in df.iterrows():

        if str(item[col1]) < str(item[col2]):
            d.append(str(item[col1])+'-'+str(item[col2]))
        else:
            d.append(str(item[col2])+'-'+str(item[col1]))
    df.insert(0, 'EdgeList', d)
    
    return df['EdgeList'].values


def centralityMeasures(adjacencyMatrix, verbose=False):
    """
    Convert the edge list to a list of edges
    
    Parameters
    ----------
    adjacencyMatrix : pandas DataFrame
        Contains the network as an adjecency matrix
    verbose: boolean
        Indicates whether the information chould be printed. By default False
        
    Return
    ------
    Returns the the network properties
    
    """
    
    
    numNodes = adjacencyMatrix.shape[0]
    G = nx.from_pandas_adjacency(adjacencyMatrix)
    
    
    degreeCentrality = nx.degree_centrality(G)
    avgDegreeCentrality = np.mean(np.array(list(degreeCentrality.values())))*numNodes
    if verbose: print('Degree Centrality: ', avgDegreeCentrality)
        
    eigenVecCentrality = nx.eigenvector_centrality(G)
    avgEigenVecCentrality = np.mean(np.array(list(eigenVecCentrality.values())))
    if verbose:  print('Eigenvector Centrality: ', avgEigenVecCentrality)
        
    averageclustering = nx.average_clustering(G)
    if verbose: print('Clustering Coefficient: ', averageclustering)
        
    betweenessCentrality = nx.betweenness_centrality(G)
    avgbetweenessCentrality = np.mean(np.array(list(betweenessCentrality.values())))
    if verbose: print('Betweeness Centrality: ', avgbetweenessCentrality) 
    
    closenessCentrality = nx.closeness_centrality(G)
    avgclosenessCentrality = np.mean(np.array(list(closenessCentrality.values())))
    if verbose: print('Closeness Centrality: ', avgclosenessCentrality)
        

    return [avgDegreeCentrality, avgEigenVecCentrality, averageclustering, avgbetweenessCentrality, avgclosenessCentrality]