import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
import os, subprocess, shutil, sys

def __calculateScore(df: pd.DataFrame, axis=1):
    return df.apply(lambda x: np.sqrt(np.sum(np.square(x))), axis=axis)

def __renameKeys(mainDf: pd.DataFrame, keyDf: pd.DataFrame, renameColumn, left_on=None):
    if left_on is not None:
        mergeDf = pd.merge(mainDf, keyDf, left_on=left_on, right_index=True, how='left', sort=False).copy()
    else:
        mergeDf = pd.merge(mainDf, keyDf, left_index=True, right_index=True, how='left', sort=False).copy()
    mergeDf.index = mergeDf[renameColumn]
    mergeDf = mergeDf.drop(renameColumn, axis=1, inplace=False)
    return mergeDf

def parsePlates(inDf: pd.DataFrame, sep: str = '._.'):
    plates = [str(i).split(sep)[1] for i in list(inDf.index)]
    updatedDf = inDf.copy()
    updatedDf['plates'] = plates
    updatedDf.set_index('plates', append=True, inplace=True)

    return updatedDf

def getPlateActivityScores(plate,\
                        compoundDf: pd.DataFrame,\
                        noCompDf: pd.DataFrame = None,\
                        map = None,\
                        activityTitles = ['pma_ActivityScores', 'noPma_ActivtyScores'],\
                        controlTitle = ['DMSO', 'PMA'],\
                        sep='._.', wellLabels = 'Wells',\
                        renameColumn = 'longname_proper'):
    wells = [str(i).split('._.')[0] for i in list(compoundDf.index.get_level_values(wellLabels))]
    plateName = list(compoundDf.index.get_level_values('plates'))

    if noCompDf is None:
        plateComp = __calculateScore(df=compoundDf.copy())
        rawData = {
            activityTitles[0]:plateComp.to_numpy(),
            'plate': plateName,
            'wells': wells
        }
    else:
        plateComp = __calculateScore(df=compoundDf.copy())
        plateNoCompDf = __calculateScore(df=noCompDf.copy())
        rawData = {
            activityTitles[0]:plateComp.to_numpy(),
            activityTitles[1]:plateNoCompDf.to_numpy(),
            'plate': plateName,
            'wells': wells
        }
    
    acScoreDf = pd.DataFrame(rawData)
    acScoreDf.sort_index(inplace=True)

    if map is not None:
        namingDf = compoundDf if noCompDf is None else noCompDf
        renamedDf = __renameKeys(mainDf=namingDf, keyDf=map, renameColumn=renameColumn, left_on='Wells')
        acScoreDf['Full Proper Name'] = list(renamedDf.index)
        acScoreDf.set_index('Full Proper Name', inplace=True)
    else:
        acScoreDf['Full Proper Name'] = list(compoundDf.index.get_level_values(wellLabels)) if noCompDf is None else list(noCompDf.index.get_level_values(wellLabels))
        acScoreDf.set_index('Full Proper Name', inplace=True)
    inclSep = lambda x: ''.join([x,sep])
    wellType = [f'CONTROL_{controlTitle[0]}' if inclSep(controlTitle[0]) in i else f'CONTROL_{controlTitle[1]}' if inclSep(controlTitle[1]) in i else 'EXPERIMENTAL' for i in list(acScoreDf.index)]
    acScoreDf['well_type'] = wellType

    return acScoreDf

def createDataScores(compDf: pd.DataFrame, noCompDf: pd.DataFrame = None, ):
    return