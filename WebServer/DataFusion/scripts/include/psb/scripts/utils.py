import numpy as np

def getHardClusters(G):
    """
    Compute hard clustering from a G factor comming from a NMTF factorization
    
    Parameters
    ----------
    G: numpy array
        Contains G factor (cluster indicator) of a NMTF factorization
        
    Return
    ------
    Returns the cluster indicator of each entry in a list.
    
    """

    return [np.argmax(G[i]) for i in range(G.shape[0])]