import xml.etree.ElementTree as ET
import pandas as pd

def parsingXML2Groups(filePath, savePath):
    """
    Pasing DrugBank XML to CSV with the groups of each
    
    Parameter
    ---------
    filePath: str
        Path with the xml file
        
    Return
    ------
        DataFrame with the drugs and the corresponding groups
    """
    
    tree = ET.parse(filePath)
    root = tree.getroot()


    
    res = []
    for drugs in root:
        t = drugs.attrib['type']
        for atr in drugs:

            if ('drugbank-id' in atr.tag)&('primary' in atr.attrib):
                dbID = atr.text

            if ('name' in atr.tag):
                dbName = atr.text    

            if 'groups' in atr.tag:
                for subgroup in atr:
                    res.append([t, dbID, dbName, subgroup.text])

    dfRes = pd.DataFrame(res, columns=['type', 'DrugBank ID', 'DrugBank Name', 'Group'])
    
    if savePath != '': dfRes.to_csv(savePath, index=False) 
    return dfRes

def parsingXML2SMILES(filePath, savePath):
    """
    Pasing DrugBank XML to CSV with SMILES of each Drugs
    
    Parameter
    ---------
    filePath: str
        Path with the xml file
        
    Return
    ------
        DataFrame with the drugs and the corresponding SMILES
    """
    
    tree = ET.parse(filePath)
    root = tree.getroot()


    
    res = []
    for drugs in root:
        resTmp = []
        resTmp.append(drugs.attrib['type'])
        for atr in drugs:

            if ('drugbank-id' in atr.tag)&('primary' in atr.attrib):
                resTmp.append(atr.text)

            if 'name' in atr.tag:
                resTmp.append(atr.text)


            found=False
            if ('calculated-properties' in atr.tag):
                for cprop in atr:
                    for prop in cprop:
                        if ('kind' in prop.tag)&('SMILES' in prop.text):
                            found = True
                        if found & ('value' in prop.tag):
                            resTmp.append(prop.text)
                            found = False

                            res.append(resTmp)
    dfRes =  pd.DataFrame(res, columns=['type', 'DrugBank ID', 'DrugBank Name', 'SMILE'])

    if savePath != '': dfRes.to_csv(savePath, index=False) 
    return dfRes

def parsingXML2Targets(filePath, savePath = ''):
    """
    Pasing DrugBank XML to CSV with Targets of each Drugs
    
    Parameter
    ---------
    filePath: str
        Path with the xml file
        
    Return
    ------
        DataFrame with the drugs and the corresponding targets
    """
    
    tree = ET.parse(filePath)
    root = tree.getroot()


    
    res = []
    for drugs in root:
        t = drugs.attrib['type']
        for atr in drugs:

            if ('drugbank-id' in atr.tag)&('primary' in atr.attrib):
                dbID = atr.text

            if ('name' in atr.tag):
                dbName = atr.text      

            if ('targets' in atr.tag):
                for targets in atr:
                    for tInfo in targets:

                        if 'polypeptide' in tInfo.tag: 
                            geneTarget = ''
                            for tInfoGene in tInfo:
                                
                                if ('gene-name' in tInfoGene.tag)&(tInfoGene.text is not None): 
                                    geneTarget = tInfoGene.text
                                    
                                #Restricting to proteins from Homo Sapiens
                                if ('organism' in tInfoGene.tag)&(geneTarget != ''):
                                    if("Humans" in tInfoGene.text):
                                        res.append([t, dbID, dbName, geneTarget])
                                        
    dfRes = pd.DataFrame(res, columns=['type', 'DrugBank ID', 'DrugBank Name', 'Gene Target'])
    
    if savePath != '': dfRes.to_csv(savePath, index=False) 
    return dfRes



def parsingXML2Categories(filePath, savePath = ''):
    """
    Pasing DrugBank XML to CSV with Category of each Drugs
    
    Parameter
    ---------
    filePath: str
        Path with the xml file
        
    Return
    ------
        DataFrame with the drugs and the corresponding categories
    """
    res = []
    for drugs in root:
        t = drugs.attrib['type']
        for atr in drugs:

            if ('drugbank-id' in atr.tag)&('primary' in atr.attrib):
                dbID = atr.text

            if ('name' in atr.tag):
                dbName = atr.text    

            if 'categories' in atr.tag:
                for cat in atr:
                    for subcat in cat:
                        if 'category' in subcat.tag:
                            c = subcat.text
                        if 'mesh-id' in subcat.tag:
                            mID = subcat.text
                            #print([t, dbID, dbName, c, mID])
                            res.append([t, dbID, dbName, c, mID])

    dfRes = pd.DataFrame(res, columns=['type', 'DrugBank ID', 'DrugBank Name', 'Category', 'Mesh-ID'])
    if savePath != '': dfRes.to_csv(savePath, index=False) 
    return dfRes