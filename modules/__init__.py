import pandas as pd, numpy as np
import Bio.Cluster as pycluster

def renameKeys(mainDf: pd.DataFrame, keyDf: pd.DataFrame, renameColumn, left_on=None, **kwargs):
    if left_on is not None:
        mergeDf = pd.merge(mainDf, keyDf, left_on=left_on, right_index=True, how='left', sort=False).copy()
    else:
        mergeDf = pd.merge(mainDf, keyDf, left_index=True, right_index=True, how='left', sort=False).copy()
    mergeDf.index = mergeDf[renameColumn]
    mergeDf = mergeDf.drop(renameColumn, axis=1, inplace=False)
    return mergeDf

def pyclusterHeatmap_pearsonComplete(inTabFile, outname, rowCluster = True, colCluster = True):
    record = pycluster.read(open(inTabFile))
    genetree, exptree = None, None
    if rowCluster:
        genetree = record.treecluster(method='m',dist='c',transpose=0)
        genetree.scale()

    if colCluster:
        exptree = record.treecluster(method='m',dist= 'c',transpose=1)
        exptree.scale()

    # genetree.scale()
    # exptree.scale()
    record.save(outname,genetree,exptree)

def parsePlates(inDf: pd.DataFrame, sep: str = '._.', plateLabelIndex = -1, **kwargs):
    try:
        plates = [str(i).split(sep)[plateLabelIndex] for i in list(inDf.index)]
    except IndexError:
        plates = [str(i).split(sep)[0] for i in list(inDf.index)]
    updatedDf = inDf.copy()
    updatedDf['plates'] = plates
    updatedDf.set_index('plates', append=True, inplace=True)

    return updatedDf

def calculateScore(df: pd.DataFrame, axis=1):
    return df.apply(lambda x: np.sqrt(np.sum(np.square(x))), axis=axis)