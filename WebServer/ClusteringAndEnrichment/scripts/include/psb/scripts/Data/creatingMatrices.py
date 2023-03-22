from creatingNetworksUtils import createBipariteMatrixFromEdgeList, createAdjacencyMatrixFromEdgeList, rawBioGRID2network, filterRepeatedInteractions
from smoothingBipartiteNetwork import smoothBipartiteNetwork
from numpy.random import choice

import pandas as pd
import numpy as np



# -----------------------------------------------------------------------------------
#
# Matrices R12, R23, L2 and L3 creation from Raw Data
# 
# -----------------------------------------------------------------------------------


def createR12(saveMatrices=True, verbose=True, pathLoad='', pathSave=''):
    """
    Create the SARS-CoV-2 to HS proteins interaction Network (R12) from the BioGRID Data
    
    Parameters
    ----------
    saveMatrices: boolean
        Indicates whther the matrices have to be saved. Default True
    verbose: boolean
        Indicates whether information of the dataset have to be printed. By default True
    pathLoad: string
        Path where the raw data can be found. Default is the same directory.
    pathSave: string
        Path where the generated data have to be saved. Default is the same directory.
        
    Return
    ------
    Returns the created network in a DataFrame.
    
    """
    

    loadPath = pathLoad+'BIOGRID-ORGANISM-Severe_acute_respiratory_syndrome_coronavirus_2-3.5.183.tab2.txt'
    # savePath = '../Data/Networks/BioGRID_PPI_SARS-CoV-2-HS_edgeList.csv'
    savePath = pathSave + '../Networks/BioGRID_PPI_SARS-CoV-2-HS_edgeList.csv'

    edgeListCoV_HS = rawBioGRID2network(loadPath, savePath, 'Official Symbol', 'physical', [], [], verbose=1)

    r12 = createBipariteMatrixFromEdgeList(edgeListCoV_HS)
    
    if saveMatrices: 
        r12.to_csv(pathSave+'Matrix_R12.csv')
        np.save(pathSave+'Matrix_R12.npy', r12.values)
    
    if verbose: print('SARS-HS Interactions has {} SARS-CoV-2 genes interacting with {} HS genes with {} interactions.'.format(r12.shape[0], r12.shape[1], edgeListCoV_HS.shape[0]))
        
    return r12



        
def createL2(saveMatrices=True, verbose=True, pathLoad='', pathSave=''):
    """
    Create the Molecular Network (L2) using the PPI and GI from BioGRID Data and Molecular Interactions from KEGG
    
    Parameters
    ----------
    saveMatrices: boolean
        Indicates whther the matrices have to be saved. Default True
    verbose: boolean
        Indicates whether information of the dataset have to be printed. By default True
    pathLoad: string
        Path where the raw data can be found. Default is the same directory.
    pathSave: string
        Path where the generated data have to be saved. Default is the same directory.
        
    Return
    ------
    Returns the created networks (adjacency and laplacian) in a DataFrame.
    
    """
    #PPI and GI from BioGRID
    loadPath = pathLoad+'BIOGRID-ORGANISM-Homo_sapiens-3.5.183.tab2.txt'
    savePath21, savePath22 = '', ''
    if saveMatrices:
        # savePath21 = '../Data/Networks/BioGRID_PPI-HS_edgeList.csv'
        # savePath22 = '../Data/Networks/BioGRID_GI-HS_edgeList.csv'
        savePath21 = pathSave + '../Networks/BioGRID_PPI-HS_edgeList.csv'
        savePath21 = pathSave + '../Networks/BioGRID_GI-HS_edgeList.csv'

    #Experimental System Type for PPI
    physicalExperimentalSystemType = ['Two-hybrid', 'Affinity Capture-Luminescence', 'Affinity Capture-Western', 'Affinity Capture-MS']

    edgeListHS_PPI = rawBioGRID2network(loadPath, savePath21, 'Official Symbol', 'physical', physicalExperimentalSystemType, ['9606'], verbose=1)
    edgeListHS_GI = rawBioGRID2network(loadPath, savePath22, 'Official Symbol', 'genetic', [], ['9606'], verbose=1)

    #MI from KEGG
    edgeListHS_MI = pd.read_csv(pathLoad+'KEGG_metabolic_network_hgnc.edgelist', sep='\t', header=None)

    #Making sure all the three lists have the same name for the columns
    edgeListHS_PPI.columns, edgeListHS_GI.columns, edgeListHS_MI.columns = [0,1], [0,1], [0,1]

    #Creating the MN form the union of the PPI, GI and MI
    edgesListHS_MN = pd.concat((edgeListHS_PPI, edgeListHS_GI)).drop_duplicates()
    edgesListHS_MN = pd.concat((edgesListHS_MN, edgeListHS_MI)).drop_duplicates()
    edgesListHS_MN = filterRepeatedInteractions(edgesListHS_MN)
    
    
    a2 = createAdjacencyMatrixFromEdgeList(edgesListHS_MN)
    a2Deg = np.diag(a2.values.sum(axis=0))
    l2 = a2Deg - a2
    

    if saveMatrices: 
        a2.to_csv(pathSave+'Matrix_A2.csv')
        np.save(pathSave+'Matrix_A2.npy', a2.values)
    if saveMatrices: 
        l2.to_csv(pathSave+'Matrix_L2.csv')
        np.save(pathSave+'Matrix_L2.npy', l2.values)
        
    if verbose: print('Molecular Network has {} HS genes with {} interactions.'.format(a2.shape[0], edgesListHS_MN.shape[0]))
        
    return a2, l2





def createR23(l2, l3, saveMatrices=True, verbose=True, pathLoad='', pathSave=''):
    """
    Create the Drug target Interaction (R23) from the DrugBanks Data
    
    Parameters
    ----------
    l2: pandas DataFrame
        Laplacian matrix with genes interactions
    l3: pandas DataFrame
        Laplacian matrix with drugs interactions
    saveMatrices: boolean
        Indicates whther the matrices have to be saved. Default True
    verbose: boolean
        Indicates whether information of the dataset have to be printed. By default True
    pathLoad: string
        Path where the raw data can be found. Default is the same directory.
    pathSave: string
        Path where the generated data have to be saved. Default is the same directory.
        
    Return
    ------
    Returns the created network in a DataFrame.
    
    """
    
    #Load Group Data
    dfDG = pd.read_csv(pathLoad+'Drug_Groups.csv')
    drugsAppExp = dfDG[dfDG['Group'].isin(['approved', 'experimental'])]['DrugBank ID'].values
    
    #Load and restrict DTI data
    dfDTI = pd.read_csv(pathLoad+'Drug_Target_Interactions.csv')
    dfDTIRestricted = dfDTI[(dfDTI['DrugBank ID'].isin(drugsAppExp))&(dfDTI['type'] == 'small molecule')]
    bipartiteDTI = createBipariteMatrixFromEdgeList(dfDTIRestricted[['Gene Target', 'DrugBank ID']])
    
    #Update bipartite between genes in l2 and drugs in l3
    r23 = pd.DataFrame(np.zeros((l2.shape[0], l3.shape[1])), index=l2.index, columns=l3.columns)
    r23.update(bipartiteDTI)
    
    if saveMatrices: 
        r23.to_csv(pathSave+'Matrix_R23.csv')
        np.save(pathSave+'Matrix_R23.npy', r23.values)
        
    if verbose: print('DTI has {} HS genes interacting with {} drugs with {} interactions.'.format(r23.shape[0], r23.shape[1], dfDTIRestricted.shape[0]))
        
        
    return r23


def createL3(saveMatrices=True, verbose=True, pathLoad='', pathSave=''):
    """
    Create the Drug Chemical Similarities (L3) from the DrugBanks Data
    
    Parameters
    ----------
    saveMatrices: boolean
        Indicates whther the matrices have to be saved. Default True
    verbose: boolean
        Indicates whether information of the dataset have to be printed. By default True
    pathLoad: string
        Path where the raw data can be found. Default is the same directory.
    pathSave: string
        Path where the generated data have to be saved. Default is the same directory.
        
    Return
    ------
    Returns the created network in a DataFrame.
    
    """
    
    #Load DCS data
    dfDCS = pd.read_csv(pathLoad+'Drugs_similarities_top5percent.csv')
    a3 = createAdjacencyMatrixFromEdgeList(dfDCS[['DrugBank ID 1', 'DrugBank ID 2']])

    a3Deg = np.diag(a3.values.sum(axis=0))
    l3 = a3Deg - a3

    if saveMatrices: 
        a3.to_csv(pathSave+'Matrix_A3.csv')
        np.save(pathSave+'Matrix_A3.npy', a3.values)
    if saveMatrices: 
        l3.to_csv(pathSave+'Matrix_L3.csv')
        np.save(pathSave+'Matrix_L3.npy', l3.values)
    if verbose: print('Drug Chemical Interaction has {} drugs with {} interactions.'.format(a3.shape[0], dfDCS.shape[0]))
        
    return a3, l3
        
    

def matricesCreation(saveMatrices=True, verbose=True, numpy=True, pathLoad='', pathSave='', alpha=0.6):
    """
    Create the matrices needed for the data fusion framework.
    
    Parameters
    ----------
    saveMatrices: boolean
        Indicates whther the matrices have to be saved. Default True
    verbose: boolean
        Indicates whether information of the dataset have to be printed. By default True
    numpy: boolean
        Indicates whether the matrices must be returned as numpy or pandas. By defaul True
    pathLoad: string
        Path where the raw data can be found. Default is the same directory.
    pathSave: string
        Path where the generated data have to be saved. Default is the same directory.
    alpha: numpy array
        The diffusion parameter to use for R12 propagated network. By default 0.6
         
         
    Return
    ------
    Returns the created networks in DataFrames.
    
    """

    # SARS-CoV-2 to HS proteins interaction Network (R12) 
    r12 = createR12(saveMatrices, verbose, pathLoad, pathSave)
        
    # Molecular Network (L2)
    a2, l2 = createL2(saveMatrices, verbose, pathLoad, pathSave)
    
    # Smooth R12
    r12Aug = smoothBipartiteNetwork(r12, a2, [alpha], pathSave+'Matrix_R12', verbose=False, saveMatrices=saveMatrices)
    if verbose: print('R12 smoothed')
    
    # Drug Chemical Similarities (L3)
    a3, l3 = createL3(saveMatrices, verbose, pathLoad, pathSave)
    
    # Drug target Interaction (R23)
    r23 = createR23(l2, l3, saveMatrices, verbose, pathLoad, pathSave)   
     
    if numpy:
        return r12Aug.values, l2.values, r23.values, l3.values, r12.values, a2.values, r23.values
        
    return r12Aug, l2, r23, l3, r12, a2, r23
    
def matricesLoad(pathLoad='', verbose=True, alpha=0.6):
    """
    Load the matrices needed for the data fusion framework.
    
    Parameters
    ----------
    pathLoad: string
        Path where the raw data can be found. Default is the same directory.
    alpha: numpy array
        The diffusion parameter to use for R12 propagated network. By default 0.6
         
    Return
    ------
    Returns the created networks in DataFrames.
    
    """

    # Smooth R12
    r12Aug = pd.read_csv(pathLoad+'Matrix_R12_'+str(alpha)+'.csv', index_col=0)
    if verbose: print('R12 loaded')
    
    # Molecular Network (L2)
    l2 = pd.read_csv(pathLoad+'Matrix_L2.csv', index_col=0)
    if verbose: print('L2 loaded')
    
    # Drug Chemical Similarities (L3)
    l3 = pd.read_csv(pathLoad+'Matrix_L3.csv', index_col=0)
    if verbose: print('L3 loaded')
    
    # Drug target Interaction (R23)
    r23 = pd.read_csv(pathLoad+'Matrix_R23.csv', index_col=0)
    if verbose: print('R23 loaded')
    
    return r12Aug, l2, r23, l3


def matricesLoadNumpy(pathLoad='', verbose=True, alpha=0.6):
    """
    Load the matrices needed for the data fusion framework.
    
    Parameters
    ----------
    pathLoad: string
        Path where the raw data can be found. Default is the same directory.
    alpha: numpy array
        The diffusion parameter to use for R12 propagated network. By default 0.6
         
    Return
    ------
    Returns the created networks in DataFrames.
    
    """

    # Smooth R12
    r12Aug = np.load(pathLoad+'Matrix_R12_'+str(alpha)+'.npy')
    if verbose: print('R12 loaded')

    # Molecular Network (L2)
    l2 = np.load(pathLoad+'Matrix_L2.npy')
    if verbose: print('L2 loaded')

    # Drug Chemical Similarities (L3)
    l3 = np.load(pathLoad+'Matrix_L3.npy')
    if verbose: print('L3 loaded')

    # Drug target Interaction (R23)
    r23 = np.load(pathLoad+'Matrix_R23.npy')
    if verbose: print('R23 loaded')

    return r12Aug, l2, r23, l3


# -----------------------------------------------------------------------------------
#
# Matrices R12, R23, L2 and L3 creation from Raw Data only using PPI
# 
# -----------------------------------------------------------------------------------

def createL2PPI(saveMatrices=True, verbose=True, pathLoad='', pathSave=''):
    """
    Create the Molecular Network (L2) using the PPI and GI from BioGRID Data and Molecular Interactions from KEGG
    
    Parameters
    ----------
    saveMatrices: boolean
        Indicates whther the matrices have to be saved. Default True
    verbose: boolean
        Indicates whether information of the dataset have to be printed. By default True
    pathLoad: string
        Path where the raw data can be found. Default is the same directory.
    pathSave: string
        Path where the generated data have to be saved. Default is the same directory.
        
    Return
    ------
    Returns the created networks (adjacency and laplacian) in a DataFrame.
    
    """
    
    edgeListHS_PPI = pd.read_csv(pathLoad+'BioGRID_PPI-HS_edgeList.csv', index_col=0)

    #Making sure all the three lists have the same name for the columns
    edgeListHS_PPI.columns  = [0,1]

    a2_PPI = createAdjacencyMatrixFromEdgeList(edgeListHS_PPI)
    a2Deg_PPI = np.diag(a2_PPI.values.sum(axis=0))
    l2_PPI = a2Deg_PPI - a2_PPI

    if verbose: print('Molecular Network has {} HS genes with {} interactions.'.format(a2_PPI.shape[0], edgeListHS_PPI.shape[0]))

    if saveMatrices:
        a2_PPI.to_csv(pathSave+'Matrix_A2.csv')
        np.save(pathSave+'Matrix_A2.npy', a2_PPI.values)
        l2_PPI.to_csv(pathSave+'Matrix_L2.csv')
        np.save(pathSave+'Matrix_L2.npy', l2_PPI.values)

    return a2_PPI, l2_PPI
        
def matricesCreationPPI(saveMatrices=True, verbose=True, numpy=True, pathLoad='', pathSave='', alpha=0.6):
    """
    Create the matrices needed for the data fusion framework when PPI is used as human interactome.
    
    Parameters
    ----------
    saveMatrices: boolean
        Indicates whther the matrices have to be saved. Default True
    verbose: boolean
        Indicates whether information of the dataset have to be printed. By default True
    numpy: boolean
        Indicates whether the matrices must be returned as numpy or pandas. By defaul True
    pathLoad: string
        Path where the raw data can be found. Default is the same directory.
    pathSave: string
        Path where the generated data have to be saved. Default is the same directory.
    alpha: numpy array
        The diffusion parameter to use for R12 propagated network. By default 0.6
         
         
    Return
    ------
    Returns the created networks in DataFrames.
    
    """

    # SARS-CoV-2 to HS proteins interaction Network (R12) 
    r12 = createR12(saveMatrices, verbose, pathLoad, pathSave)
        
    # Molecular Network (L2) afected by changing the human interactome network
    a2, l2 = createL2PPI(saveMatrices, verbose, '../Data/Networks/', pathSave+'PPIasHumanInteractome/')
    
    # Smooth R12  afected by changing the human interactome network
    r12Aug = smoothBipartiteNetwork(r12, a2, [alpha], pathSave+'PPIasHumanInteractome/'+'Matrix_R12', verbose=False, saveMatrices=saveMatrices)
    if verbose: print('R12 smoothed')
    
    # Drug Chemical Similarities (L3)
    a3, l3 = createL3(saveMatrices, verbose, pathLoad, pathSave)
    
    # Drug target Interaction (R23)  afected by changing the human interactome network
    r23 = createR23(l2, l3, saveMatrices, verbose, pathLoad, pathSave+'PPIasHumanInteractome/')   
     
    if numpy:
        return r12Aug.values, l2.values, r23.values, l3.values, r12.values, a2.values, r23.values
        
    return r12Aug, l2, r23, l3, r12, a2, r23


def matricesLoadNumpyPPI(pathLoad='', verbose=True, alpha=0.6):
    """
    Load the matrices needed for the data fusion framework when PPI is used as human interactome.
    
    Parameters
    ----------
    pathLoad: string
        Path where the raw data can be found. Default is the same directory.
    alpha: numpy array
        The diffusion parameter to use for R12 propagated network. By default 0.6
         
    Return
    ------
    Returns the created networks in DataFrames.
    
    """
    
    # Smooth R12
    r12Aug = np.load(pathLoad+'Matrix_R12_'+str(alpha)+'.npy')
    if verbose: print('R12 loaded')

    # Molecular Network (L2)
    l2 = np.load(pathLoad+'PPIasHumanInteractome/Matrix_L2.npy')
    if verbose: print('L2 loaded')

    # Drug Chemical Similarities (L3)
    l3 = np.load(pathLoad+'Matrix_L3.npy')
    if verbose: print('L3 loaded')

    # Drug target Interaction (R23)
    r23 = np.load(pathLoad+'PPIasHumanInteractome/Matrix_R23.npy')
    if verbose: print('R23 loaded')

    return r12Aug, l2, r23, l3


        
# -----------------------------------------------------------------------------------
#
# Matrices G1, G2, G3 H12, H23 Initialization 
# 
# -----------------------------------------------------------------------------------


def matricesRandomAcolInitializationNumpy(r12, r23, l3, k1, k2, k3, s=None):
    """
    Inizialize the matrices with random Acol
    
    Parameters
    ----------
    r12: numpy array
         Relational matrix between viral proteins and genes
    r23: numpy array
         Relational matrix between genes and drugs
    l3: numpy array
        Laplacian matrix with drugs interactions
    k1: integer
        Indicates the number of cluster for the viral proteins
    k2: integer
        Indicates the number of cluster for the genes
    k3: integer
        Indicates the number of cluster for the drugs
    s: integer
       seed for the randomization 
        
    Return
    ------
    Returns the matrices g1, g2, g3, h12 and h23 with random Acol
    
    """
    
    if r12.shape[1] != r23.shape[0]:
        return 'Matrix R12 must have same number of columns that rows in R23.'

    epsilon = 1e-5
    if s is not None: np.random.seed(s)
    n1, n2 = r12.shape[0], r12.shape[1]
    n3 = r23.shape[1]

    g1 = np.zeros((n1, k1))
    p = round(n2/5)
    for col in range(k1):
        columns = choice(n2, p)
        g1[:, col] = np.mean(r12[:, columns], axis=1) + epsilon

    g2 = np.zeros((n2, k2))
    p = round(n3/10)
    for col in range(k2):
        columns = choice(n3, p)
        g2[:, col] = np.mean(r23[:, columns], axis=1) + epsilon


    g3 = np.random.rand(n3, k3) + epsilon

    h12 = np.random.rand(k1, k2) + epsilon
    h23 = np.random.rand(k2, k3) + epsilon

    return g1, g2, g3, h12, h23

def matricesRandomAcolInitialization(r12, r23, l3, k1, k2, k3, s=None):
    """
    Inizialize the matrices with random Acol
    
    Parameters
    ----------
    r12: pandas DataFrame
         Relational matrix between viral proteins and genes
    r23: pandas DataFrame
         Relational matrix between genes and drugs
    l3: pandas DataFrame
        Laplacian matrix with drugs interactions
    k1: integer
        Indicates the number of cluster for the viral proteins
    k2: integer
        Indicates the number of cluster for the genes
    k3: integer
        Indicates the number of cluster for the drugs
    s: integer
       seed for the randomization 
        
    Return
    ------
    Returns the matrices g1, g2, g3, h12 and h23 initializated with random Acol
    
    """
    
    if r12.shape[1] != r23.shape[0]:
        return 'Matrix R12 must have same number of columns that rows in R23.'
    
    epsilon = 1e-5
    if s is not None: np.random.seed(s)
    n1, n2 = r12.shape[0], r12.shape[1]
    n3 = r23.shape[1]
    
    g1 = np.zeros((n1, k1)) 
    p = round(n2/5)
    for col in range(k1):
        columns = choice(n2, p)
        g1[:, col] = np.mean(r12[r12.columns[columns]], axis=1) + epsilon
    
    g2 = np.zeros((n2, k2)) 
    p = round(n3/10)
    for col in range(k2):
        columns = choice(n3, p)
        g2[:, col] = np.mean(r23[r23.columns[columns]], axis=1) + epsilon
        
    
    g3 = np.random.rand(n3, k3) + epsilon
    
    h12 = np.random.rand(k1, k2) + epsilon
    h23 = np.random.rand(k2, k3) + epsilon
    
    return g1, g2, g3, h12, h23

def matricesRandomInitialization(r12, r23, k1, k2, k3, s=None):
    """
    Inizialize the matrices randomly
    
    Parameters
    ----------
    r12: pandas DataFrame
         Relational matrix between viral proteins and genes
    r23: pandas DataFrame
         Relational matrix between genes and drugs
    k1: integer
        Indicates the number of cluster for the viral proteins
    k2: integer
        Indicates the number of cluster for the genes
    k3: integer
        Indicates the number of cluster for the drugs
    s: integer
       seed for the randomization 
        
    Return
    ------
    Returns the matrices g1, g2, g3, h12 and  h23 randomly initializated
    
    """
    
    if r12.shape[1] != r23.shape[0]:
        return 'Matrix R12 must have same number of columns that rows in R23.'
    
    if s is not None: np.random.seed(s)
    epsilon = 1e-5
    n1, n2 = r12.shape[0], r12.shape[1]
    n3 = r23.shape[1]
    
    g1 = np.random.rand(n1, k1) + epsilon
    g2 = np.random.rand(n2, k2) + epsilon
    g3 = np.random.rand(n3, k3) + epsilon
    
    h12 = np.random.rand(k1, k2) + epsilon
    h23 = np.random.rand(k2, k3) + epsilon
    
    return g1, g2, g3, h12, h23


def restrictSVD(X, J,K,L, k1, k2):
    """
    Restrics the component of the SVD (X = JKL) to the number of columns needed
    
    Parameters
    ----------
    X: numpy array
       containing the decomposed matrix
    J: numpy array
       containing the first factor of the decomposition
    K: numpy array
       containing the middle factor of the decomposition
    L: numpy array
       containing the last factor of the decomposition
    k1: integer
        Indicates the number of cluster for the viral proteins
    k2: integer
        Indicates the number of cluster for the genes
    s: integer
       seed for the randomization 
        
    Return
    ------
    Returns the restricted factors.
    
    """
        
    epsilon = 1e-5
    n, m = X.shape        

    
    J = J[:n, :k1]
    U = np.where(J > 0., J, epsilon)

    S = np.full((k1,k2), epsilon)
    for i in range(min(k1, k2)):
        S[i][i] = K[i]
        
    L = L[:m, :k2]
    V = np.where(L > 0., L/3., epsilon)[:m, :k2]

    return U,S,V

def matricesSVDInitialization(r12, r23, k1, k2, k3):
    """
    Inizialize the matrices with SVD decomposition
    
    Parameters
    ----------
    r12: pandas DataFrame
         Relational matrix between viral proteins and genes
    r23: pandas DataFrame
         Relational matrix between genes and drugs
    k1: integer
        Indicates the number of cluster for the viral proteins
    k2: integer
        Indicates the number of cluster for the genes
    k3: integer
        Indicates the number of cluster for the drugs
        
    Return
    ------
    Returns the matrices g1, g2, g3, h12 and h23 initializated with the SVD.
    
    """
    
    if r12.shape[1] != r23.shape[0]:
        return 'Matrix R12 must have same number of columns that rows in R23.'
    

    g1,h12,g21 = np.linalg.svd(r12) 
    g1,h12,g21 = restrictSVD(r12, g1, h12, g21, k1, k2)
    
    g22,h23,g3 = np.linalg.svd(r23) 
    g22,h23,g3 = restrictSVD(r23, g22, h23, g3, k2, k3)
    
    g2 = g22+g21/2
    
    return g1, g2, g3, h12, h23

def matricesSVDInitializationOneRelation(r23, k2, k3):
    """
    Inizialize the matrices with SVD decomposition
    
    Parameters
    ----------
    r23: pandas DataFrame
         Relational matrix
    k2: integer
        Indicates the number of cluster for the first component
    k3: integer
        Indicates the number of cluster for the second compoent
        
    Return
    ------
    Returns the matrices initializated with the SVD.
    
    """

    g2,h23,g3 = np.linalg.svd(r23) 
    g2,h23,g3 = restrictSVD(r23, g2, h23, g3, k2, k3)

    
    return g2, g3, h23