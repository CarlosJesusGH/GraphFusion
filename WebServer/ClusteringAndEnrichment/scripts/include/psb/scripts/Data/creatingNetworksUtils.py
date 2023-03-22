import pandas as pd
import numpy as np

def createAdjacencyMatrixFromEdgeList(edgeList, undirected=True):
    """
    Convert raw data from edgeList to Adjacency Matrix
    
    Parameters
    ----------
    edgeList: pandas DataFrame 
        DataFrame with a network in an edgelist format

    Return
    ------
    Pandas DataFrame containing the adjacency matrix of the network.
    """
    
    #Duplicating edges if it is an undirected network
    edgeList.columns = ['col1', 'col2']
    if undirected:
        dfTmp1 = edgeList[['col1', 'col2']]
        dfTmp2 = edgeList[['col2', 'col1']]
        dfTmp2.columns =  ['col1', 'col2']
        edgeList = pd.concat((dfTmp1, dfTmp2))
    edgeList.insert(edgeList.shape[1], 'value', np.ones(edgeList.shape[0]))
    
    #Transforming the edges to a adjacency matrix form
    dfPivoted = edgeList.pivot(index='col1', columns='col2', values='value')
    
    col1, col2 = edgeList.columns[0], edgeList.columns[1]
    proteins1, proteins2 = edgeList[col1].values, edgeList[col2].values
    proteinsList = list(np.unique(np.concatenate((proteins1, proteins2))))
    
    #Inserting the edges into the adjacency matrix
    dfAdj = pd.DataFrame(np.zeros((len(proteinsList), len(proteinsList))), index=proteinsList, columns=proteinsList)
    dfAdj.update(dfPivoted)
    return dfAdj

def createBipariteMatrixFromEdgeList(edgeList):
    """
    Convert raw data from edgeList to Bipartite Matrix
    
    Parameters
    ----------
    edgeList: pandas DataFrame 
        DataFrame with network in edgeList format (each column is one part of the component)

    Return
    ------
    Pandas DataFrame containing the bipartite matrix of the network.
    """
    
    
    col1, col2 = edgeList.columns[0], edgeList.columns[1]
    proteinsList1, proteinsList2 = list(edgeList[col1].unique()), list(edgeList[col2].unique())
    
    bipartiteMatrix = np.zeros((len(proteinsList1), len(proteinsList2)))
    for ind, item in edgeList.iterrows():
        bipartiteMatrix[proteinsList1.index(item[col1]), proteinsList2.index(item[col2])] = 1.0
    
    return pd.DataFrame(bipartiteMatrix, index=proteinsList1, columns=proteinsList2)

       
def filterRepeatedInteractions(edgeList):
    """
    Filter repeated interactions from a edge list
    
    Parameters
    ----------
    edgeList: pandas DataFrame 
        DataFrame with a network in an edgelist format

    Return
    ------
    Pandas DataFrame containing the edge list without repeated interactions
    """
    
    col1, col2 = edgeList.columns[0], edgeList.columns[1]

    d = []
    for ind, item in edgeList.iterrows():

        if str(item[col1]) < str(item[col2]):
            d.append(str(item[col1])+'-'+str(item[col2]))
        else:
            d.append(str(item[col2])+'-'+str(item[col1]))
    edgeList.insert(0, 'dummy', d)
    
    return edgeList.drop_duplicates(subset='dummy').drop(['dummy'], axis=1)


def rawBioGRID2network(loadPath, savePath, name, experimentSystemType, experimental, taxonomyIDs, verbose=0):
    """
    Convert raw data from BioGRID to Network
    
    Parameters
    ----------
    loadPath: str 
        File path with the Raw data from BioGRID with format tab2.
    savePath: str
        File path where to save the created adjacency matrix
    name: str [Entrez Gene | Official Symbol | Systematic Name ]
        Name of the nomenclature used to select and filter the data.
    experimentSystemType: str [genetic | physical]
        Experiment System Type wanted.
    experimental: list
        List of the Exprimental Systems wanted. If it is empty all are selected.
    taxonomyIDs: list
        List of taxonomyIDs of the species wanted. If it is empty all are selected.
        
     Return
    ------
    Pandas DataFrame containing the network matrix with the type specified in typeOfMatrix.
    """
        
    #Obtaining Data
    df = pd.read_csv(loadPath, sep='\t')
    
    #Checking if the name is in the data
    if not (name +' Interactor A' in df.columns)&(name+' Interactor B'in df.columns): 
        print('The nomenclarute {} passed by the parameter Name not in the data.'.format(name)) 
        return

    if experimentSystemType not in df['Experimental System Type'].unique(): 
        print('The experiment system type {} passed not in the data.'.format(experimentSystemType)) 
        return
    
    #Filtering by Experimental System Type
    df = df[df['Experimental System Type'] == experimentSystemType]
    
    #Filtering by Experimental System
    if len(experimental) > 0:
        df = df[df['Experimental System'].isin(experimental)]
     
    #Filtering by Organism
    if len(taxonomyIDs) > 0:    
        df = df[(df['Organism Interactor A'].isin(taxonomyIDs))&(df['Organism Interactor B'].isin(taxonomyIDs))] 
        
    #Filtering self interactions
    df = df[df[name + ' Interactor A'] != df[name + ' Interactor B']]
        
    #Reducing to one interactions found by different method
    df = df.drop_duplicates(subset=[name + ' Interactor A', name + ' Interactor B'])
    
    #Reudcing to one, repeated interactions found as the oposite interactor
    edgeList = filterRepeatedInteractions(df[[name + ' Interactor A', name + ' Interactor B']])

        
    if savePath != '': edgeList.to_csv(savePath)
    return edgeList