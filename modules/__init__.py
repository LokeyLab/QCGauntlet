import modules.clusterPlates
import modules.controlCorr
import modules.cpActivityScores
import modules.cpActivityScoresV2
import pandas as pd, numpy as np

def renameKeys(mainDf: pd.DataFrame, keyDf: pd.DataFrame, renameColumn) -> pd.DataFrame:
    mergeDf = pd.merge(mainDf, keyDf, left_index=True, right_index=True, how='left', sort=False).copy()
    mergeDf.index = mergeDf[renameColumn]
    mergeDf = mergeDf.drop(renameColumn, axis=1, inplace=False)
    return mergeDf