
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import os

import sys
sys.path.append('../scripts/Data/')
from creatingNetworksUtils import createAdjacencyMatrixFromEdgeList


#-----------------------------------------------------------
#  Compute gene sets
#-----------------------------------------------------------

def computeGeneSets(adj, VI, DEG, pathSave, verbose=True, save=True):
    """
    Create the gene sets from a network
    
    Parameters
    ----------
    adj: pandas DataFrame
        Contains the adjacency matrix of the network
    VI: list or numpy array
        Contains the viral interactor genes name
    DEG: list or numpy array
        Contains the differentially expressed genes name 
    pathSave: string
        Path where the generated data have to be saved
    verbose: boolean
        Indicates whether information of the dataset have to be printed. By default True
    save: boolean
        Indicates whther the matrices have to be saved. By default True
    
    """
    
    if verbose: print(adj.columns.shape[0], 'whole network')
    VI_adj = [g for g in VI if g in adj.columns]
    DEG_adj = [g for g in DEG if g in adj.columns]
    
    background = adj.columns
    
    background = [g for g in background if g not in VI_adj]
    if verbose: print(len(VI_adj), ' VI in network')
    if verbose: print(len(background), ' Background')
    background = [g for g in background if g not in DEG]
    if verbose: print(len(DEG_adj), ' DEG in network', len(DEG), ' DEG total') 
    if verbose: print(len(background), ' Background')
    
    G = nx.from_pandas_adjacency(adj)
    
    VI_neighbours = set([n for gene in VI_adj for n in G.neighbors(gene)])
    VI_neighbours = [g for g in VI_neighbours if (g not in VI) and (g not in DEG)]
    DEG_neighbours = set([n for gene in DEG_adj for n in G.neighbors(gene)])
    DEG_neighbours = [g for g in DEG_neighbours if (g not in VI) and (g not in DEG)]  
    
    commonNeighbours = set([g for g in VI_neighbours if g in DEG_neighbours])
    if verbose: print(len(commonNeighbours), ' Common neighbours')
    background = [g for g in background if g not in commonNeighbours]
    if verbose: print(len(background), ' Background')
    
    VI_neighbours_unique = [g for g in VI_neighbours if g not in commonNeighbours]
    DEG_neighbours_unique = [g for g in DEG_neighbours if g not in commonNeighbours]
    
    background = [g for g in background if g not in VI_neighbours_unique]
    if verbose: print(len(VI_neighbours_unique), ' VI-unique neighbours')
    if verbose: print(len(background), ' Background') 
    background = [g for g in background if g not in DEG_neighbours_unique]
    if verbose: print(len(DEG_neighbours_unique), ' DEG-unique neighbours')
    if verbose: print(len(background), ' Background')
    
    if save:
        dfDegNeigh = pd.DataFrame(DEG_neighbours, columns=['Gene'])
        dfDegNeigh.to_csv(pathSave+'DEGNeighboursGenes.csv', index=False)
        dfVINeigh = pd.DataFrame(VI_neighbours, columns=['Gene'])
        dfVINeigh.to_csv(pathSave+'VINeighboursGenes.csv', index=False)
        
        dfDegNeighUnique = pd.DataFrame(DEG_neighbours_unique, columns=['Gene'])
        dfDegNeighUnique.to_csv(pathSave+'DEGNeighboursUniqueGenes.csv', index=False)
        dfVINeighUnique = pd.DataFrame(VI_neighbours_unique, columns=['Gene'])
        dfVINeighUnique.to_csv(pathSave+'VINeighboursUniqueGenes.csv', index=False)
        dfComNeigh = pd.DataFrame(commonNeighbours, columns=['Gene'])
        dfComNeigh.to_csv(pathSave+'CommonNeighboursGenes.csv', index=False)

        dfDegNeighUnique.insert(1, 'Gene Description' , ['DEG-unique neighbor']*dfDegNeighUnique.shape[0])
        dfVINeighUnique.insert(1, 'Gene Description' , ['VI-unique neighbor']*dfVINeighUnique.shape[0])
        dfComNeigh.insert(1, 'Gene Description' , ['Common neighbor']*dfComNeigh.shape[0])
        
        dfDEG = pd.DataFrame(DEG_adj, columns=['Gene'])
        dfDEG.insert(1, 'Gene Description' , ['DEG']*dfDEG.shape[0])
        dfVI = pd.DataFrame(VI_adj, columns=['Gene'])
        dfVI.insert(1, 'Gene Description' , ['VI']*dfVI.shape[0])

        dfBackground = pd.DataFrame(background, columns=['Gene'])
        dfBackground.insert(1, 'Gene Description' , ['Background']*dfBackground.shape[0])
        
        dfRes = pd.concat((dfDEG, dfVI))
        dfRes = pd.concat((dfRes, dfVINeighUnique))
        dfRes = pd.concat((dfRes, dfDegNeighUnique))
        dfRes = pd.concat((dfRes, dfComNeigh))
        dfRes = pd.concat((dfRes, dfBackground))
        dfRes.to_csv(pathSave+'allGenes.csv', index=False)
        
        
#-----------------------------------------------------------
#  Network statistics
#-----------------------------------------------------------       
        
        
def computeDegree(network):
    """
    Compute the degree of all the nodes in the network.
    
    Parameters
    ----------
    network: pandas DataFrame
        Contains the adjacency matrix of the network
        
    Return
    ------
    Returns a pandas DataFrame with the degree of each node in the network
    """
    
    G = nx.from_pandas_adjacency(network)
    degreesTmp = nx.degree_centrality(G)
    degrees = pd.DataFrame([[k,v] for k, v in degreesTmp.items()], columns=['Gene', 'Degree'])
    degrees['Degree'] = (degrees['Degree']*network.shape[0]).apply(lambda x: round(x))

    return degrees       


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
    
    dfAll = pd.DataFrame()
    degreeCentrality = nx.degree_centrality(G)
    degrees = pd.DataFrame([[k,v] for k, v in degreeCentrality.items()], columns=['Gene', 'Average Degree'])
    degrees['Average Degree'] = (degrees['Average Degree']*numNodes).apply(lambda x: round(x))   
    dfAll = degrees
    if verbose: print('Degrees computed')
    
    eigenVecCentrality = nx.eigenvector_centrality(G)
    eigenVec = pd.DataFrame([[k,v] for k, v in eigenVecCentrality.items()], columns=['Gene', 'Eigenvector Centrality'])
    dfAll = pd.merge(dfAll, eigenVec)
    if verbose: print('EigenVectors computed')    
        
    betweenessCentrality = nx.betweenness_centrality(G)
    betCen = pd.DataFrame([[k,v] for k, v in betweenessCentrality.items()], columns=['Gene', 'Betweeness Centrality'])
    dfAll = pd.merge(dfAll, betCen)
    if verbose: print('Betweeness Centrality computed')  
        
    closenessCentrality = nx.closeness_centrality(G)
    cloCen = pd.DataFrame([[k,v] for k, v in closenessCentrality.items()], columns=['Gene', 'Closeness Centrality'])
    dfAll = pd.merge(dfAll, cloCen)
    if verbose: print('Closeness Centrality computed')  
    
    clusteringCoef = nx.clustering(G)
    clustCoef = pd.DataFrame([[k,v] for k, v in clusteringCoef.items()], columns=['Gene', 'Clustering Coefficient'])
    dfAll = pd.merge(dfAll, clustCoef)
    if verbose: print('Clustering Coeficient computed')  
        
    return dfAll
        
#-----------------------------------------------------------
#  Graphlet count
#-----------------------------------------------------------


def loadData(pathFile):
    """
    Create the adjacency matrix from the edgelist of the network.
    
    Parameters
    ----------
    pathFile: string
        Indicates the path where the edge list can be found.
        
    Return
    ------
    Returns a pandas DataFrame with the adjacency matrix of the network.
    
    """
    
    edgesListHS = pd.read_csv(pathFile, index_col=0)
    network = createAdjacencyMatrixFromEdgeList(edgesListHS)
    genesNetwork = network.columns
    print('Total number of genes ', len(genesNetwork))
          
    return network  

def _createEdgeList(G, fileSave):
    """
    Create the edge list in the format l'orca needs and save it in a file.
    
    Parameters
    ----------
    G: networkx graph
       Contains the network
    fileSave: string
    
        
    """
    
    nx.write_edgelist(G, fileSave, data=False)
    N, M = G.number_of_nodes(), G.number_of_edges()
    
    with open(fileSave, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.write("%s %s\n"%(N,M) + content)
        
        
def createOrcaFile(adj, fileName, path='../Data/OrcaFormatFiles'):
    """
    Create the orca file and the mappings
    
    Parameters
    ----------
    adj: pandas DataFrame
        Contains the adjacency matrix of the network
    fileName: string
        Indicates the path where the edge list can be found.
        
    Return
    ------
    Returns two dictionaries containing the mapping between genes and the identifier in the orca file.
    
    """
    
    mainComponent = nx.from_pandas_adjacency(adj) 
    
    labelMapping   = {name:n for n,name in enumerate(mainComponent)}
    reverseMapping = {value:key for key,value in labelMapping.items()}

    G = nx.relabel_nodes(mainComponent, labelMapping) 

    print("{}/{}.txt".format(path,fileName))
    txtFilePath = os.path.abspath("{}/{}.txt".format(path,fileName))
    
    _createEdgeList(G, txtFilePath)
    
    return labelMapping, reverseMapping