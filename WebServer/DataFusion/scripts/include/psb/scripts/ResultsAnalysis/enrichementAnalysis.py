import statsmodels.stats.multitest as ssm
from scipy.special import binom,comb
from scipy.stats import hypergeom
from gprofiler import GProfiler
from functools import reduce
import pandas as pd
import numpy as np
import operator

import sys
sys.path.append('../scripts/')
from utils import getHardClusters

#--------------------------------------------------------------------
#   Extract Clusters
#--------------------------------------------------------------------

# def extractClusters(names, fileName):
def extractClusters(names, G):
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

    dfClusters = pd.DataFrame(getHardClusters(G), index=names).reset_index() 
    dfClusters.columns = ['Entity', 'Cluster']
    
    size = dfClusters.groupby('Cluster').count().reset_index()
    
    clusters = [list(dfClusters[dfClusters['Cluster'] == cluster]['Entity'].values) for cluster in dfClusters.sort_values('Cluster')['Cluster'].unique()]
    
    return clusters


#--------------------------------------------------------------------
#   Load annotations data
#--------------------------------------------------------------------

def loadDrugAnnotations(drugs, verbose=False):
    """
    Loades the drug annotations
    
    Parameters
    ----------
    drugs: list
        Contains the name of the drugs
    verbose: boolean
        Indicates whether information of the dataset have to be printed. By default False
    Return
    ------
    Return a dictionary where the keys are the annotations and the values are list of drugs with that annotation.
    
    """
    
    drugCategory = pd.read_csv('../Data/Raw/Drug_Categories.csv')

    drugs = pd.read_csv('../Data/Names/Drugs.csv')['Drugs'].values
    if verbose: print(drugs.shape[0], ' drugs')

    categoriesForOurDrugs = drugCategory[drugCategory['DrugBank ID'].isin(drugs)]['Category'].unique()
    if verbose: print(categoriesForOurDrugs.shape[0], ' categories')
        
    categoriesPerDrug = drugCategory[drugCategory['DrugBank ID'].isin(drugs)].groupby('DrugBank ID').Category.count()
    
    drugCatDict = {drug : drugCategory[drugCategory['DrugBank ID'] == drug]['Category'].values for drug in drugs}
    
    categoriesToDrugs = {cat : drugCategory[drugCategory['Category'] == cat]['DrugBank ID'].values for cat in categoriesForOurDrugs}
    
    return categoriesToDrugs

def loadGeneAnnotations(aspect, genes, verbose=False):
    """
    Loades the gene annotations
    
    Parameters
    ----------
    aspect: boolean
        Indicates the aspect in Gene Ontology (i.e., Biological Process, Molecular Function or Cellular Component)
    genes: list
        Contains the name of the drugs
    verbose: boolean
        Indicates whether information of the dataset have to be printed. By default False
        
    Return
    ------
    Return a dictionary where the keys are the annotations and the values are list of genes with that annotation.
    
    """
        
    path = '../Data/Annotations/GoOntology/' 

    filePath = path+'GOAnnotation_{}_{}.csv'.format('Homo_sapiens', aspect)
    dfAnnotations = pd.read_csv(filePath)
    if verbose: print(len(dfAnnotations['Official Symbol'].unique()))

    annotatedProteins = dfAnnotations['Official Symbol'].unique()
    if verbose: print(len(annotatedProteins), 'genes annotated with ', aspect, ' out of ', len(genes))
    
    dfAnnotationsNetwork = dfAnnotations[dfAnnotations['Official Symbol'].isin(genes)]
    
    annotationsToGenes = {annotation : dfAnnotationsNetwork[dfAnnotationsNetwork['GO ID'] == annotation]['Official Symbol'].values for annotation in dfAnnotationsNetwork['GO ID'].unique()}

    return annotationsToGenes



#--------------------------------------------------------------------
#   Enrichment Analysis Clusters
#--------------------------------------------------------------------
def _computePercentages(clusters, annotationsToMolecules, clusterEnrichedAnnotations, clusterEnrichedMolecules):
    """
    Compute the percentages of enriched clusters, annotations and molecules (e.g., gener or drugs). 
    
    Parameters
    ----------
    clusters : list of sets  
        Each set contains the number of molecules in that cluster
        
    annotationsToMolecules: dictionary ({annotation : {molecules}})
        Dictionary containing for each annotation a set of the molecules annotated with it.
        
    clusterEnrichedAnnotations: dictionary ({annotation : {molecules}})
        Dictionary containing for each annotation a set of the molecules that are enriched with it.    
    
    clusterEnrichedMolecules: dictionary ({cluster : {molecules}})
        Dictionary containing for each cluster a set of the molecules that are enriched with it. 
    
    Returns
    -------
    annotationsEnriched :  float
        Indicating percentage of annotations enriched
    
    clustersEnriched : float
        Indicating percentage of clusters enriched
    
    entitiesEnriched : float
        Indicating percentage of entities enriched
    """                   
    
    #Percentage of enriched GO terms               
    annotationsEnriched = (len(set(reduce(operator.concat,clusterEnrichedAnnotations.values()))) / len(annotationsToMolecules.keys()))*100
    
    #Percentage of enriched clusters   
    enrichedClusters = [k for k, v in clusterEnrichedAnnotations.items() if len(v) > 0]
    clustersEnriched = (len(enrichedClusters) / len(clusters))*100
    
    #Percentage of enriched proteins
    moleculesEnriched = (len(set(reduce(operator.concat,clusterEnrichedMolecules.values()))) / len(set(reduce(operator.concat,clusters))))*100

    return(annotationsEnriched, clustersEnriched, moleculesEnriched)

def enrichmentAnalysis(clusters, annotationsToMolecules):
    """
    Perform the enrichement analysis of various clusters given the molecules clustered and its annotations. 
    
    Parameters
    ----------
    clusters : list of sets  
        Each set contains the number of molecules in that cluster
        
    annotationsToMolecules: dictionary ({annotation : {molecules}})
        Dictionary containing for each annotation a set of the genes annotated with it.
        
    Returns
    -------
    annotationsEnriched :  float
        Indicating percentage of annotations enriched
    
    clustersEnriched : float
        Indicating percentage of clusters enriched
    
    entitiesEnriched : float
        Indicating percentage of entities enriched
    """
          
    #Compute M (annotated proteins in the network)
    M = len(set(reduce(operator.concat,clusters)))

    clusterEnrichedAnnotations, clusterEnrichedMolecules = {}, {} 
    for cInd, cluster in enumerate(clusters):
        
   
        #Compute N (annotated proteins in the cluster)
        N = len(cluster)
        
        #TODO: see if with other structures the computation time is reduced.
        annoTmp = []
        pvalues = []
        for i, ann in enumerate(annotationsToMolecules.keys()):

            annotatedMolecules = annotationsToMolecules[ann]
            annotatedMoleculesInCluster = [molecule for molecule in annotatedMolecules if molecule in cluster] 
 
            if len(annotatedMoleculesInCluster) > 0:
                #Compute K (proteins with annotation ann)
                K = len(annotatedMolecules)

                #Compute X (proteins in C and with annotation ann)
                X = len(annotatedMoleculesInCluster)

                #Compute hypergeometric Test
                pvalues.append(hypergeom.sf(X-1, M, K, N))

                annoTmp.append(ann)
            
        if len(pvalues) > 0:
            #Correct for multipletesting
            correction = ssm.multipletests(pvalues, alpha=0.05, method='fdr_bh',is_sorted=False, returnsorted=False)

            annotatedEnriched = np.asarray(annoTmp)[correction[0]]
            if len(annotatedEnriched) > 0:
                clusterEnrichedAnnotations[cInd] = annotatedEnriched.tolist()

                #If statistics needed to be computed, create cluster to enriched molecules 
                if len(clusterEnrichedAnnotations) > 0:
                    enrichedMolecules = []
                    for enrichedAnnotation in clusterEnrichedAnnotations[cInd]:
                        for molecule in annotationsToMolecules[enrichedAnnotation]:
                            if molecule in clusters[cInd]: 
                                if molecule not in enrichedMolecules:
                                    enrichedMolecules.append(molecule)

                    clusterEnrichedMolecules[cInd] = enrichedMolecules
            else:
                clusterEnrichedAnnotations[cInd] = []
                clusterEnrichedMolecules[cInd] = []
        else:
            clusterEnrichedAnnotations[cInd] = []
            clusterEnrichedMolecules[cInd] = []
                        
         
    annotationsEnriched, clustersEnriched, entitiesEnriched = _computePercentages(clusters, annotationsToMolecules, clusterEnrichedAnnotations, clusterEnrichedMolecules)
    
    return annotationsEnriched, clustersEnriched, entitiesEnriched

#--------------------------------------------------------------------
#   Enrichment Analysis Genes
#--------------------------------------------------------------------

def enrichmentAnalysisGprofiler(listOfGenes):
    """
    Performs an enrichment analysis using the software Gprofiler
    
    Parameters
    ----------
    listOfGenes: list
        Contains the genes 
        
    Return
    ------
    Return a pandas DataFrame with all the terms enriched in the set of genes.
    
    """
        
    gp = GProfiler(return_dataframe=True)
    dfRes = gp.profile(organism='hsapiens', query=listOfGenes, sources=["GO","KEGG","REAC","CORUM"])

    dfFinal = dfRes[['p_value', 'source', 'native', 'name', 'term_size', 'query_size', 'intersection_size', 'precision', 'recall']].sort_values(['source', 'p_value'])
    dfFinal.columns = ['p_value', 'source', 'term_id', 'term_name', 'term_size', 'query_size', 'intersection_size', 'precision', 'recall']
    
    return dfFinal
