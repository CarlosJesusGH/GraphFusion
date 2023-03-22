import pandas as pd
import numpy as np

#Iterative part
def networkPropagation(bipartite_0, normalizedNetwork, alpha = 0.6, eps = 6, verbose=False):
    """
    Iterative process to propagate the influence of each node on a bipartite matrix over its neighbours in a network [Vanunu et al]. 
    
    Parameters
    ----------
    bipartite_0: numpy array
        Original bipartite matrix.
    
    normalizedNetwork: numpy array
        Normalized matrix of the network over the which the bipartite network is propagated.
    
    alpha: float
        Parameter to set the distance of diffusion through network. By default 0.6
    
    eps: int
        Exponent of the difference between iteraction as stop criterion. By default 6
    
    verbose: boolean 
        Indicates information of the iterations and error have to be printed. By default False
        
    Return
    ------
    Propagated bipartite matrix.
    
    """
    
    #Initialization
    bipartite_old = bipartite_0
    stop = False
    it = 0
    
    while not stop:

        bipartite_new = alpha*np.dot(bipartite_old, normalizedNetwork) + (1-alpha)*bipartite_0

        #Stop criterion
        err = np.linalg.norm(bipartite_new - bipartite_old, ord='fro') 
        stop = err - 10**(-eps) < 0

        #Updating the iteration
        bipartite_old = bipartite_new
        it +=1
        
        if (verbose)&(it % 10 == 0): print(it, err)

    if verbose: print(it, err)
    return bipartite_new

def smoothBipartiteNetwork(bipartite, network, alphas, savePath, eps=6, verbose=False, saveMatrices=True):
    """
    Propagation of the influence of each node on a bipartite matrix over its neighbours in a network [Vanunu et al]. Saves all the resulting propations with the different alphas in the given savePath.
    
    Parameters
    ----------
    bipartite_0: numpy array
        Original bipartite matrix.
    
    network: numpy array
        Network over the which, after normalizing it, the bipartite network is propagated.
    
    alphas: list
        Parameter to set the distance of diffusion through network. By default 0.6
        
    savePath: string
        Path were the resulting smoothed bipartites networks will be saved.
    
    eps: int
     Exponent of the difference between iteraction as stop criterion. By default 6
    
    verbose: boolean 
        Indicate information of the iterations and error have to be printed. By default False
        
    Return
    ------
    Returning the smoothed bipartite network, using the last alpha provided. All the resulting networks are saved in the path provided in savePath.
    
    """
    
    #Augment bipartite matrix to network nodes
    augmentedBipartite = pd.DataFrame(np.zeros((bipartite.shape[0], network.shape[1])), index=bipartite.index, columns=network.columns)
    augmentedBipartite.update(bipartite)
    

    #Normalize network
    networkDegInv = np.diag(1 / network.sum(axis=0))
    normalizedNetwork = np.dot(network.values, networkDegInv)
    
    for alpha in alphas:
        smoothedBipartite = networkPropagation(augmentedBipartite.values, normalizedNetwork, alpha, verbose=verbose)
        dfRes = pd.DataFrame(smoothedBipartite, index=bipartite.index, columns=network.columns)
        if saveMatrices: 
            dfRes.to_csv(savePath+'_'+str(alpha)+'.csv')
            np.save(savePath+'_'+str(alpha)+'.npy', dfRes.values)
                    
    return dfRes