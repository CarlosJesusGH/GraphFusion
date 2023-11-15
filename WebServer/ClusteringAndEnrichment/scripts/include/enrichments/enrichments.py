import numpy as np
import h5py
import pandas as pd
import sys
import os

# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))

import sys
# sys.path.append('../psb/scripts/')

# print("SCRIPT_DIR", SCRIPT_DIR)

sys.path.append(os.path.join(sys.path[0], '../psb/scripts/')); # print("sys.path", sys.path)
from ResultsAnalysis.enrichementAnalysis import *



# ---------------------------------------------------------------

def loadEntityAnnotations(entities, anno_filePath, verbose=False):
    """
    Loades the annotations
    
    Parameters
    ----------
    aspect: boolean
        Indicates the aspect in Gene Ontology (i.e., Biological Process, Molecular Function or Cellular Component)
    entities: list
        Contains the name of the genes, drugs, etc
    verbose: boolean
        Indicates whether information of the dataset have to be printed. By default False
        
    Return
    ------
    Return a dictionary where the keys are the annotations and the values are list of entities (genes/drugs/etc) with that annotation.
    
    """
    # if verbose: print("", )
    # aspects = ['BiologicalProcess', 'MolecularFunction', 'CellularComponent']
    # aspect= aspects[0]
    # path = '../Data/Annotations/GoOntology/' 
    # filePath = path+'GOAnnotation_{}_{}.csv'.format('Homo_sapiens', aspect)
    dfAnnotations = pd.read_csv(anno_filePath, header=None, delimiter="\t")
    print("dfAnnotations.shape", dfAnnotations.shape)
    if verbose: print("dfAnnotations.iloc[0:10,:]\n", dfAnnotations.iloc[0:10,:])
    # if verbose: print(len(dfAnnotations['Official Symbol'].unique()))
    # annotatedProteins = dfAnnotations['Official Symbol'].unique()
    # if verbose: print(len(annotatedProteins), 'genes annotated with ', aspect, ' out of ', len(entities))
    # annotatedEntities = pd.read_csv(op_dir + "/" + entitylist_filename).iloc[:,0].values
    # if verbose: print(len(annotatedEntities), 'entities annotated out of ', len(entities))
    # dfAnnotationsNetwork = dfAnnotations[dfAnnotations['Official Symbol'].isin(entities)]
    dfAnnotationsNetwork = dfAnnotations[dfAnnotations.iloc[:,0].isin(entities)]
    if verbose: print("dfAnnotationsNetwork", dfAnnotationsNetwork)
    # annotationsToGenes = {annotation : dfAnnotationsNetwork[dfAnnotationsNetwork['GO ID'] == annotation]['Official Symbol'].values for annotation in dfAnnotationsNetwork['GO ID'].unique()}
    annotationsToGenes = {annotation : dfAnnotationsNetwork[dfAnnotationsNetwork.iloc[:,1] == annotation].iloc[:,0].values for annotation in dfAnnotationsNetwork.iloc[:,1].unique()}
    if verbose:
        print("type(annotationsToGenes)", type(annotationsToGenes))
        print("dict(list(annotationsToGenes.items())[:10]", dict(list(annotationsToGenes.items())[:10]))
    return annotationsToGenes


# ---------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------

args = sys.argv[1:]
op_dir, fact_name, entitylist_filename, enrichments_anno = args[0], args[1], args[2], args[3]

print("args", args)

import matplotlib.pyplot as plt

# with h5py.File(op_dir + "/" + fact_name, "r") as f:
#     factor = np.array(f.get('dataset'))
factor = np.loadtxt(open(op_dir + "/" + fact_name, "rb"), delimiter="\t", skiprows=0)
print("factor.shape", factor.shape)

# entities = range(factor.shape[0])
# clusters = extractClusters(factor)
clusters = np.load(op_dir + "/" + "clusters.npy", allow_pickle=True)
# cluster_lens = [len(cluster) for cluster in clusters]
# plt.bar(range(len(cluster_lens)), sorted(cluster_lens, reverse=True))

""" ----------------------------------------------------------------
# create random annotations
if True:
    import random
    categoriesToDrugs = {}
    for category in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
        # print(category)
        categoriesToDrugs[category] = []
        for i in range(random.randint(1,10)):
            categoriesToDrugs[category].append(entities[random.randint(0,len(entities)-1)])
---------------------------------------------------------------- """

entities = pd.read_csv(op_dir + "/" + entitylist_filename, header=None).iloc[:,0].values
# print("len(entities)", len(entities))
# print("entities", entities)
categoriesToEntities = loadEntityAnnotations(entities, enrichments_anno, verbose=False)
# print("categoriesToEntities", categoriesToEntities)
# print("len(categoriesToEntities)", len(categoriesToEntities))

# compute enrichments using psb script in DataFusion/scripts/include/psb/scripts/ResultsAnalysis/enrichementAnalysis.py
categoriesEnriched, clustersEnriched, entitiesEnriched, enrichedClustersIdx = enrichmentAnalysis(clusters, categoriesToEntities)
# print("categoriesEnriched, clustersEnriched, entitiesEnriched, enrichedClusters:", categoriesEnriched, clustersEnriched, entitiesEnriched, enrichedClustersIdx)
dfEntitiesEnrichments = pd.DataFrame([categoriesEnriched, clustersEnriched, entitiesEnriched], index=['Clusters of Entities', 'Annotations', 'Entities'], columns=['']).transpose()
# print(dfDrugsEnrichments)

fig = dfEntitiesEnrichments.plot(kind='bar', rot=0, color=['#1f78b4', '#e31a1c', '#6a3d9a'], width=0.13, 
                            # figsize=(20, 16), fontsize=26
                            ).get_figure()

# set axis labels and title
# plt.xlabel('Clusters of Entities')
plt.ylabel('Percentage of enriched (%)')
plt.title('Enrichments for Clusters of Entities')

fig.savefig(op_dir + "/" + "enrichments_for_clusters.svg")

import csv
with open(op_dir + "/" + "clusters.csv", 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        clusters = list(reader)
# get the clusters that are enriched using the indices
enrichedClustersList = [clusters[i] for i in enrichedClustersIdx]
# save the enriched clusters to a file
with open(op_dir + "/" + "clusters_enriched.csv", "w", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerows(enrichedClustersList)