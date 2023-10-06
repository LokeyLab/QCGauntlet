from modules import *
import pandas as pd, numpy as np
import os, sys, subprocess, shutil
import time

def formatDf(compDf: pd.DataFrame, noCompDf: pd.DataFrame = None, key=None, controls = ['DMSO','PMA'], sep='._.', renameColumn='longname_proper', **kwargs):
    reformattedDfs = []

    compDf = renameKeys(mainDf=compDf, keyDf=key, renameColumn=renameColumn) if key is not None else compDf
    compDf = parsePlates(inDf=compDf, sep=sep, **kwargs)

    for control in controls:
        sepCompDf = compDf[compDf.index.get_level_values(renameColumn).str.contains(f'{control}{sep}')]
        sepCompDf = sepCompDf.sort_index(level='plates')
        reformattedDfs.append(sepCompDf)
    
    if noCompDf is not None:
        noCompDf = renameKeys(mainDf=noCompDf, keyDf=key, renameColumn=renameColumn) if key is not None else noCompDf
        noCompDf = parsePlates(inDf=noCompDf, sep=sep, **kwargs)

        for control in controls:
            sepNoCompDf = noCompDf[noCompDf.index.get_level_values(renameColumn).str.contains(f'{control}{sep}')]
            sepNoCompDf = sepNoCompDf.sort_index(level='plates')
            reformattedDfs.append(sepNoCompDf)

    res = pd.concat(reformattedDfs, axis=0, copy=True)
    return res.reset_index(level='plates', drop=True)

def genTreeViewClustMap(inDf: pd.DataFrame, outname, rowCluster=True, colCluster = True):
    try:
        os.mkdir('.temp/')
    except:
        shutil.rmtree('.temp/')
        time.sleep(0.1) # i need program to sleep in order to call the next command
        os.mkdir('.temp/')

    inDf.to_csv('.temp/out.tsv', sep='\t')
    pyclusterHeatmap_pearsonComplete(inTabFile='.temp/out.tsv', outname=outname, rowCluster=rowCluster, colCluster=colCluster)
    shutil.rmtree('.temp/')
    return
    
    