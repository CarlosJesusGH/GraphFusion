from statannot import add_stat_annotation
import matplotlib.pyplot as plt
import matplotlib_venn as venn
import seaborn as sns
import pandas as pd
import numpy as np


#-----------------------------------------------------------
#  Enrichment Analysis
#-----------------------------------------------------------

def plotEnrichments(dfGenes, dfDrugs, saveFile=None):
    """
    Plot percentage of enrichments for genes and drugs 
    
    Parameters
    ----------
    dfGenes: pandas DataFrame
        Contains the percentage of enrichments for the genes
    dfDrugs:
        Contains the percentage of enrichments for the drugs
    saveFile : string
        Indicates the path and file name where the plot must be save. If the value is None the plot is not saved. By default None

    """
    

    f, axarr = plt.subplots(1,2, dpi=400, sharey=True)

    dfGenes.plot.bar(rot=0, ax=axarr[0], color=['#1f78b4', '#e31a1c', '#6a3d9a'],)
    dfDrugs.plot.bar(rot=0, ax=axarr[1], color=['#a6cee3', '#fb9a99', '#cab2d6'], width=0.13)
    
    axarr[0].set_ylim((0,100))
    axarr[1].set_ylim((0,100))
    axarr[0].set_ylabel('Percentage of enriched (%)')
    axarr[0].legend(ncol=3, bbox_to_anchor=(1.92, 1.25))
    axarr[1].legend(ncol=3, bbox_to_anchor=(0.91, 1.15))
    axarr[0].tick_params(axis ='x', which ='both', length = 0) 
    axarr[1].tick_params(axis ='both', which ='both', length = 0) 
    plt.subplots_adjust(wspace=0.00, top=0.80)
    axarr[0].grid(axis='y',ls="--", alpha=0.15)
    axarr[1].grid(axis='y',ls="--", alpha=0.15)
    
    if saveFile != None: plt.savefig(saveFile)
    plt.show()   
    
#-----------------------------------------------------------
#  DTIs Association Scores - PR and ROC curves 
#-----------------------------------------------------------      
    
def plotAssociationScores(valuesNotInOriginal, alreadyPaired_inReconstructed, threshold, saveFile=None):
    """
    Plot distribution of the association scores
    
    Parameters
    ----------
    valuesNotInOriginal :  list
        Contains the scores of those values not in the original DTI
    alreadyPaired_inReconstructed : list
        Contains the scores of those values in the original DTI
    threshold : float
        Indicates the threshold used to restric the DTIs
    saveFile : string
        Indicates the path and file name where the plot must be save. If the value is None the plot is not saved. By default None

    """
        
    f, ax = plt.subplots(dpi=400)
    plt.grid(ls="--", alpha=0.15)
    plt.yscale("log")
    
    b = plt.hist(valuesNotInOriginal, bins=50, alpha=0.75, label='New drug-gene pairs')
    b = plt.hist(alreadyPaired_inReconstructed, bins=50, alpha=0.5, label='Original DTIs')
    
    plt.axvline(threshold, c='black', linestyle='--', label='Threshold = %0.3f' % threshold)
    plt.xlabel('Association scores')
    plt.ylabel('Density (log-scale)')
    plt.title('Distribution of the association scores')
    plt.legend()

    if saveFile != None: plt.savefig(saveFile)
    plt.show()   
    
    
def plotPRCurve(precision, recall, maxF1, threshold, precisionMaxF1, recallMaxF1, pr_auc, saveFile=None):
    """
    Plot Precission-recall curve
    
    Parameters
    ----------
    precision :  list
        Contains the precision for each threshold
    recall : list
        Contains the recall for each threshold
    maxF1 : float
        Indicates the maximum F1-score
    threshold : float
        Indicates the threshold associated with the maxF1
    precisionMaxF1 : float
        Indicates the presicion associated with the maxF1
    recallMaxF1 : float
         Indicates the recall associated with the maxF1
    pr_auc : float
         Indicates the area under the precision-recall curve
    saveFile : string
        Indicates the path and file name where the plot must be save. If the value is None the plot is not saved. By default None

    """
    f, ax = plt.subplots(dpi=400)
    plt.grid(ls="--", alpha=0.15)
    ax.plot(recall, precision,label='PR curve (PR-AUC = %0.3f)' % pr_auc)
    ax.set_aspect('equal')
    plt.axhline(precisionMaxF1, c='black')
    plt.axvline(recallMaxF1, c='black')
    ax.annotate('Maximum f1-score \n f1-score   = {:.3f} \n threshold = {:.3f}'.format(maxF1, threshold), 
                xy=(recallMaxF1, precisionMaxF1),  xycoords='data',
                xytext=(0.3, 0.65), textcoords='axes fraction',
                arrowprops=dict(facecolor='black', width=0.01),
                horizontalalignment='center', verticalalignment='top',
                )


    plt.ylabel('Precision')
    plt.xlabel('Recall')
    plt.title('Precision Recall Curve')
    plt.legend(loc="lower left")
    plt.subplots_adjust(left=0.1, right=0.9)
   
    if saveFile != None: plt.savefig(saveFile)
    plt.show()  
    

def plotTwoPRCurve(precisions, recalls, maxF1s, thresholds, precisionMaxF1s, recallMaxF1s, pr_aucs, saveFile=None):
    """
    Plot two Precission-recall curves
    
    Parameters
    ----------
    precisions :  list of list
        Contains the precisions for each curve to plot 
    recalls : list
        Contains the recalls for each curve to plot
    maxF1s : list of float
        Indicates the maximum F1-score for each curve to plot
    thresholds : list of float
        Indicates the threshold associated with the maxF1 for each curve to plot
    precisionMaxF1s : list of float
        Indicates the presicion associated with the maxF1 for each curve to plot
    recallMaxF1s : list of float
         Indicates the recall associated with the maxF1 for each curve to plot
    pr_aucs : list of float
         Indicates the area under the precision-recall curve for each curve to plot
    saveFile : string
        Indicates the path and file name where the plot must be save. If the value is None the plot is not saved. By default None

    """
        
    f, ax = plt.subplots(dpi=400)
    plt.grid(ls="--", alpha=0.15)


    ax.plot(recalls[0], precisions[0],label='PR curve MIN (PR-AUC = %0.3f)' % pr_aucs[0], color='darkorange')
    ax.set_aspect('equal')

    ax.annotate('MIN \n Max f1-score \n f1-score   = {:.3f} \n threshold = {:.3f}'.format(maxF1s[0], thresholds[0]), 
                xy=(recallMaxF1s[0], precisionMaxF1s[0]),  xycoords='data',
                xytext=(0.35, 0.50), textcoords='axes fraction',
                arrowprops=dict(facecolor='black', width=0.001),
                horizontalalignment='center', verticalalignment='top',
                )

    ax.plot(recalls[1], precisions[1],label='PR curve PPI (PR-AUC = %0.3f)' % pr_aucs[1], color='darkred')
    ax.set_aspect('equal')

    ax.annotate('PPI \n Max f1-score \n f1-score   = {:.3f} \n threshold = {:.3f}'.format(maxF1s[1], thresholds[1]), 
                xy=(recallMaxF1s[1], precisionMaxF1s[1]),  xycoords='data',
                xytext=(0.25, 0.85), textcoords='axes fraction',
                arrowprops=dict(facecolor='black', width=0.001),
                horizontalalignment='center', verticalalignment='top',
                )

    plt.ylabel('Precision')
    plt.xlabel('Recall')
    plt.title('Precision Recall Curve')
    plt.legend(loc="lower left")
    plt.subplots_adjust(left=0.1, right=0.9)
    
    if saveFile != None: plt.savefig(saveFile)
    plt.show()
    


def plotROCCurve(fpr, tpr, roc_auc, saveFile=None): 
    """
    Plot ROC curve
    
    Parameters
    ----------
    fpr : numpy array
        Indicates the false positive rate for each threshold
    tpr : numpy array
        Indicates the false positive rate for each threshold
    roc_auc : float
        Indicates the area under the ROC curve 
    saveFile : string
        Indicates the path and file name where the plot must be save. If the value is None the plot is not saved. By default None

    """
    
    f, ax = plt.subplots(dpi=400)
    lw = 2
    plt.grid(ls="--", alpha=0.15)
    
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--',label='Random (ROC-AUC = 0.5)')
    plt.plot(fpr, tpr, color='darkorange',lw=lw, label='ROC curve (ROC-AUC = %0.3f)' % roc_auc)
    
    plt.legend(loc="lower right")
    ax.set_aspect('equal')
    plt.xlim([-0.025, 1.0])
    plt.ylim([0.0, 1.05])
    
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic Curve')

    if saveFile != None: plt.savefig(saveFile)
    
      
    
def plotTwoROCcurves(fprs, tprs, roc_aucs, saveFile=None):  
    """
    Plot two ROC curve
    
    Parameters
    ----------
    fprs : numpy array
        Indicates the false positive rate for each curve
    tprs : numpy array
        Indicates the false positive rate for each curve
    roc_aucs : float
        Indicates the area under the ROC curve for each curve
    saveFile : string
        Indicates the path and file name where the plot must be save. If the value is None the plot is not saved. By default None

    """
    f, ax = plt.subplots(dpi=400)
    lw = 2
    plt.grid(ls="--", alpha=0.15)

    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--',label='Random (ROC-AUC = 0.5)')
    plt.plot(fprs[0], tprs[0], color='darkorange', lw=lw, label='ROC curve MIN (ROC-AUC = %0.3f)' % roc_aucs[0])
    plt.plot(fprs[1], tprs[1], color='darkred', lw=lw, label='ROC curve PPI (ROC-AUC = %0.3f)' % roc_aucs[1])

    plt.legend(loc="lower right")
    ax.set_aspect('equal')
    plt.xlim([-0.025, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic Curve')
    
    
    if saveFile != None: plt.savefig(saveFile)
    plt.show()


#-----------------------------------------------------------
#  Graphlet Counts 
#-----------------------------------------------------------    

def plotGDVDifferentSetsSameNetwork(fileName, outFilePath, reverseMapping, geneSets, nameSubGeneSets, colors, saveFile=None):
    """
    Plot GDV for different sets of the same network
    
    Parameters
    ----------
    fileName : string
        Indicates the file where the graphlet cound are saved in Orca Style
    outfilePath : 
        Indicates the path where the file in the fileName is saved. 
    reverseMapping : dictionary
        Contains the node id as a key and the gene name as  value
    geneSets : list of lists
        Contains the different genes sets 
    nameSubGeneSets : list of string
        Contains the names of the genes sets in the same order as the sets in geneSets
    colors : list of strings
        Contains the color to be used to plot the counts of each gene set in the same order as the sets in geneSets
    saveFile : string
        Indicates the path and file name where the plot must be save. If the value is None the plot is not saved. By default None

    """
        
    fig, ax = plt.subplots(dpi=400, figsize=(8,8))
    plt.grid(True, which="major", ls="--", alpha=0.45)

    columnnNames = [i for i in range(15)]
    orcaCounts = pd.read_csv("{}/{}.out".format(outFilePath, fileName), delimiter=' ', names=columnnNames)
    orcaCounts = orcaCounts.rename(index=reverseMapping)
    
    orcaCountsLogScale = np.log(orcaCounts)
    orcaCountsLogScale[orcaCountsLogScale < 0] = 0
    
    
    for geneSet, nameSubGeneSet, color in zip(geneSets, nameSubGeneSets, colors):
        orcaCountsLogScaleSet =  orcaCountsLogScale.loc[geneSet]

        ax.plot(range(0,15), np.mean(orcaCountsLogScaleSet), label = nameSubGeneSet, c=color, linewidth=3.0)
        ax.fill_between(range(0,15), np.mean(orcaCountsLogScaleSet)+np.std(orcaCountsLogScaleSet), np.mean(orcaCountsLogScaleSet)-np.std(orcaCountsLogScaleSet),color=color, alpha=0.1)
        
    ax.set_xlabel('Orbit', fontsize=14)
    ax.set_ylabel('Count (Log)' ,fontsize=14)
    plt.legend(bbox_to_anchor=(1.02, 0.95), borderaxespad=0., fontsize=16) #
    ax.set_xticks(np.arange(0, 15))
    ax.set_yticks(np.arange(0, 18,1.5))
    
    #Highlight the orbits that are not significantly different
    noSignificant = [[1,9], [4,13.6], [5,12.4], [8,8.5], [9,11.1]]
    for nS in noSignificant:
        plt.plot(nS[0], nS[1], 'o', ms=20, mec='k', mfc='none', mew=2)

    plt.tick_params(length=2, width=2, labelsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    

    if saveFile != None: plt.savefig(saveFile,bbox_inches='tight',dpi=500)
    plt.show()
    
    
def plotGDVDifferentNetworks(fileNames, outFilePath, reverseMappings, nameNetowks, saveFile=None):
    """
    Plot GDV for different networks
    
    Parameters
    ----------
    fileNames : list of string
        Indicates the file where the graphlet cound of the different networks are saved in Orca Style
    outfilePath : 
        Indicates the path where the files in the fileName are saved. 
    reverseMappings : list of dictionary
        Contains the node id as a key and the gene name as value for the different networks in the same order as the fileNames in fileNames
    nameNetowks : list of string
        Contains the names of the networks in the same order as the fileNames in fileNames
    saveFile : string
        Indicates the path and file name where the plot must be save. If the value is None the plot is not saved. By default None

    """
    fig, ax = plt.subplots(dpi=400, figsize=(8,8))
    plt.grid(True, which="major", ls="--", alpha=0.45)

    columnnNames = [i for i in range(15)]

    for fileName, reverseMapping, nameNetowks in zip(fileNames, reverseMappings, nameNetowks):
        orcaCounts = pd.read_csv("{}/{}.out".format(outFilePath, fileName), delimiter=' ', names=columnnNames)
        orcaCounts.columns.name = 'Orbit' 
        orcaCounts = orcaCounts.rename(index=reverseMapping)
    
        orcaCountsLogScale = np.log(orcaCounts)
        orcaCountsLogScale[orcaCountsLogScale < 0] = 0


        plt.plot(range(0,15), np.mean(orcaCountsLogScale), label = nameNetowks, linewidth=3.0)
        plt.fill_between(range(0,15), np.mean(orcaCountsLogScale)+np.std(orcaCountsLogScale), np.mean(orcaCountsLogScale)-np.std(orcaCountsLogScale),alpha=0.1)
        
    ax.set_xlabel('Orbit', fontsize=14)
    ax.set_ylabel('Count (Log)' ,fontsize=14)
    plt.title(' ', fontweight='bold',fontsize=19)
    plt.legend(bbox_to_anchor=(0.99, 0.99), borderaxespad=0., fontsize=16)
    plt.xticks(np.arange(0, 15))
    plt.yticks(np.arange(0, 18,1.5))

    plt.tick_params(length=2, width=2, labelsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    if saveFile != None: plt.savefig(saveFile, bbox_inches='tight',dpi=500)
    plt.show()
    
#-----------------------------------------------------------
#  Plot Neighbors overlap
#-----------------------------------------------------------    
    
def plotNeighborsOverlap(firstSet, secondSet, saveFile=None):
    """
    Plot overlap between VI and DEG neighbors
    
    Parameters
    ----------
    fistset : list 
        Containing the gene that are VI neighbors
    secondset : list 
        Containing the gene that are DEG neighbors
    saveFile : string
        Indicates the path and file name where the plot must be save. If the value is None the plot is not saved. By default None


    """
    plt.figure(figsize=(6,6))
    
    out = venn.venn2(subsets =(set(firstSet), set(secondSet)), set_labels = ('', ''), set_colors=("#1f78b4", "#ff7f00"), alpha = 0.7)
    
    for text in out.set_labels:
        text.set_fontsize(18)
    for text in out.subset_labels:
        text.set_fontsize(18)

        
    plt.annotate('Common neighbors', xy=out.get_label_by_id('11').get_position() - np.array([0, 0.05]), xytext=(0,-20),ha='center', textcoords='offset points', fontsize=18)
    out.get_patch_by_id('11').set_color('#33a02c')
    plt.annotate('VI neighbors', xy=out.get_label_by_id('10').get_position() - np.array([0, 0.05]), xytext=(30,-100),
    ha='center', textcoords='offset points', fontsize=18)

    plt.annotate('DEG neighbors', xy=out.get_label_by_id('01').get_position() - np.array([0, 0.05]), xytext=(-50,-100),
    ha='center', textcoords='offset points', fontsize=18)
    plt.tight_layout()
    
    if saveFile != None: plt.savefig(saveFile)
    plt.show() 

    
def _annotated_label(ax, label, positionX, postionY=-0.05):
    """
    Annotate the different boxes of the box plot
    
    Parameters
    ----------
    ax : matplotlib axes
        Indicates the axes
    label: string
        Indicated the label to be displayed
    positionX : float
        Indicates the position on the X axis for the label
    postionY : float
        Indicates the position on the Y axis for the label. By default -0.05
    """
    
    ax.annotate(label, xy=(0.0,0.0),  xycoords='axes fraction', xytext=(positionX,postionY), textcoords='axes fraction', horizontalalignment='center', verticalalignment='center', fontsize=14)
    
def _annotated_mean(ax, means, name, positionX, postionY=0.5):
    """
    Annotate the different boxes of the box plot
    
    Parameters
    ----------
    ax : matplotlib axes
        Indicates the axes
    means : pandas DataFrame
        Contains the degree mean of each gene set.
    name: string
        Indicates the mean of which gene set to be displayed
    positionX : float
        Indicates the position on the X axis for the label
    postionY : float
        Indicates the position on the Y axis for the label. By default -0.05
    """
    
    ax.annotate('{:.2f}'.format(means.loc[name].values[0]), xy=(0.0,0.0),  xycoords='axes fraction', xytext=(positionX,postionY), textcoords='axes fraction', horizontalalignment='center', verticalalignment='center',fontsize=14)
        
def plotBoxPlotDegreeComparison(dfDegree, saveFile=None):
    """
    Box plot of the degree of the different gene sets
    
    Parameters
    ----------
    dfDegree: pandas DataFrame
        Containing the degree of each node
    saveFile : string
        Indicates the path and file name where the plot must be save. If the value is None the plot is not saved. By default None


    """
    
    fig, ax = plt.subplots(dpi=400, figsize=(10,5))
    plt.yscale('log')
    plt.grid(True, which="major", ls="--", alpha=0.45)

    #Defining the colors
    my_pal = {'VI' : "#7fb9d7", 'DEG' : "#fdb456", 'VI-unique neighbor' : "#1f78b4", 'DEG-unique neighbor': "#ff7f00", 'Common neighbor' : '#33a02c', 'Background': "#a4a4a4"}

    box_plot = sns.boxplot(x="Gene Set", y="Degree", data=dfDegree, ax=ax, palette=my_pal, saturation=1, order=['Background', 'VI', 'DEG',  'Common neighbor', 'VI-unique neighbor', 'DEG-unique neighbor'])
    ax.set_xlabel('')
    ax.set_xticklabels('')

    for patch in box_plot.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, .7))

    means = dfDegree.groupby('Gene Set').mean()
        
    #Labelling X axis
    _annotated_label(ax, 'Background \n genes', 0.075, postionY=-0.08)
    _annotated_label(ax, 'VI', 0.075+0.17)
    _annotated_label(ax, 'DEG', 0.075+0.17*1.95)
    _annotated_label(ax, 'Common \n neighbors', 0.075+0.17*3.05 , postionY=-0.08)
    _annotated_label(ax, 'VI-unique \n neighbors', 0.075  +0.17*4, postionY=-0.08)
    _annotated_label(ax, 'DEG-unique \n neighbors', 0.075 +0.17*5, postionY=-0.08)

    #Labelling mean of the boxplots
    _annotated_mean(ax, means, 'Background', 0.085, 0.15)
    _annotated_mean(ax, means, 'VI', 0.085+0.165, 0.5)
    _annotated_mean(ax, means, 'DEG', 0.085+0.165*2, 0.45)
    _annotated_mean(ax, means, 'Common neighbor', 0.085+0.165*3+0.004, 0.52)
    _annotated_mean(ax, means, 'VI-unique neighbor', 0.085+0.165*4+0.006, 0.305)
    _annotated_mean(ax, means, 'DEG-unique neighbor', 0.085+0.165*5+0.007, 0.37)


    plt.ylabel('Degree (Log)', fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    if saveFile != None: plt.savefig(saveFile)
    plt.show() 
    
    
#-----------------------------------------------------------
#  Plots Comparison constituent matrices with MIN
#-----------------------------------------------------------    
        
def plotThreeOverlapSets(firstSet, secondSet, thirdSet, saveFile):
    """
    Plot overlap between VI and DEG neighbors
    
    Parameters
    ----------
    fistset : list 
        Contains the first set
    secondset : list 
        Contains the second set
    thirdset : list 
        Contains the third set
    saveFile : string
        Indicates the path and file name where the plot must be save. If the value is None the plot is not saved. By default None


    """
    plt.figure(figsize=(6,6))
    out = venn.venn3([set(firstSet), set(secondSet), set(thirdSet)], set_labels = ('PPI', 'GI', 'MI'))
    for text in out.set_labels:
        text.set_fontsize(18)
    for x in range(len(out.subset_labels)):
        if out.subset_labels[x] is not None:
            out.subset_labels[x].set_fontsize(15)

    plt.tight_layout()
    if saveFile != None: plt.savefig(saveFile)
    plt.show() 
