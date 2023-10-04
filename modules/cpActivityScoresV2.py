import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
import os, subprocess, shutil, sys

def __calculateScore(df: pd.DataFrame, axis):
    return df.apply(lambda x: np.sqrt(np.sum(np.square(x))), axis=axis)

def __renameKeys(mainDf: pd.DataFrame, keyDf: pd.DataFrame, renameColumn):
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