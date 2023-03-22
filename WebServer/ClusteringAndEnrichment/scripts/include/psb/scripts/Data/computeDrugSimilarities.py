from rdkit.Chem import AllChem
from rdkit import DataStructs
from rdkit import Chem

import pandas as pd

def computeSimilarities(saveData=True, verbose=False, percentage=0.05, pathLoad='', pathSave = ''):
    """
    Compute the similarities between drugs
    
    Parameters
    ----------
    saveData: boolean
        Indicates whther the matrices have to be saved. Default True
    verbose: boolean
        Indicates whether information of the dataset have to be printed. By default False
    percentage: float
        Indicates the percentage of drug-drug relations to be keep after sorting them by similarity. By default 0.05
    pathLoad: string
        Path where the raw data can be found. Default is the same directory.
    pathSave: string
        Path where the generated data have to be saved. Default is the same directory.

         
    Return
    ------
    Returns the all the drug-drug similarities relation and the top "percentage"% drug-drug similarities relation
    
    """
    #Load Data
    dfSMILES = pd.read_csv(pathLoad+'Drug_SMILES.csv')    
    
    dfDG = pd.read_csv(pathLoad+'Drug_Groups.csv')
    drugsAppExp = dfDG[dfDG['Group'].isin(['approved', 'experimental'])]['DrugBank ID'].values
    
    #Restrict dfSMILES to drugs approved and experimental
    dfAppExp = df[df['DrugBank ID'].isin(drugsAppExp)]
    
    #Prepare DataFrame
    dfTmp = dfAppExp[['DrugBank ID', 'SMILE']].set_index('DrugBank ID')
    drugs = dfTmp.index.values

    #Compute Fingerprint for each SMILE
    fingerPrintsNotPossible = []
    fingerPrints = []
    for i, d1 in enumerate(drugs):
        try:
            mol = Chem.MolFromSmiles(dfTmp.loc[d1, 'SMILE'])
            mfp = AllChem.GetMACCSKeysFingerprint(mol)
            fingerPrints.append(mfp)
        except:
            fingerPrintsNotPossible.append(d1)
    if verbose: print(len(resNotPossible), ' drugs with SMILE not compatible.')
        
        
    #Restrict the data to those with Fingerprint 
    dfTmp = dfAppExp[~dfAppExp['DrugBank ID'].isin(resNotPossible)]
    print(dfTmp.shape)

    #Preparing DataFrame
    dfTmp = dfTmp[['DrugBank ID', 'SMILE']].set_index('DrugBank ID')
    drugs = dfTmp.index.values

    #Add the finger prints in the DataFrame
    dfTmp.insert(0, 'FingerPrint', fingerPrints)


    #Compute the Tanimoto similarity for each pair of drugs
    res = []
    for i, d1 in enumerate(drugs):

        for d2 in drugs[i+1:]:
            sim = DataStructs.TanimotoSimilarity(dfTmp.loc[d1, 'FingerPrint'],dfTmp.loc[d2, 'FingerPrint'])
            res.append([d1, d2, sim])

        if verbose: print(d1, 'Done')
    dfRes = pd.DataFrame(res, columns=['DrugBank ID 1', 'DrugBank ID 2', 'Similarity'])

    if saveData: dfRes.sort_values('Similarity', ascending=False).to_csv(pathSave+'Drugs_similarities.csv', index=False)


    #Comput top x%
    topPpercent = int(round((dfRes.shape[0]*percentage)))
    topSim = dfRes.loc[topPpercent]['Similarity']
    dfRestopPpercent = dfRes[dfRes['Similarity'] >= topSim]

    if saveData:  dfRestopPpercent[['DrugBank ID 1','DrugBank ID 2']].to_csv(pathSave+'Drugs_similarities_top5percent.csv', index=False)
        
    return dfRes, dfRestopPpercent