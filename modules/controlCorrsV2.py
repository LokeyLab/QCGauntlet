import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
import os
from matplotlib.backends.backend_pdf import PdfPages
from modules import *


def calcCorreplations(name: str, df: pd.DataFrame):
    corr = df.transpose().corr(method="pearson")
    corr = np.tril(corr.values, k=-1).flatten()
    corr = corr[corr != 0]
    return name, corr


def plotCorrs(corrs: np.ndarray, title: str, ax):
    sns.histplot(data=corrs, ax=ax, kde=True, bins=30)
    ax.set_title(title)
    ax.set_xlim([-1, 1])
    return


def generateControlCorrsAnalysis(
    compDf: pd.DataFrame,
    outName: str,
    key: pd.DataFrame,
    noCompDf: pd.DataFrame = None,
    controlList=[],
    threshold=0.5,
    **kwargs,
):
    renameCol = kwargs.get("renameColumn", "longname_proper")
    sep = kwargs.get("sep", "._.")
    compDf = renameKeys(mainDf=compDf, keyDf=key, renameColumn=renameCol)
    compDf = parsePlates(inDf=compDf, **kwargs)
    compDfgroup = compDf.groupby(level="plates")

    noCompDfgroup = [(None, None) for _ in range(len(compDfgroup))]
    if noCompDf is not None:
        noCompDf = renameKeys(mainDf=noCompDf, keyDf=key, renameColumn=renameCol)
        noCompDf = parsePlates(inDf=noCompDf, **kwargs)
        noCompDfgroup = noCompDf.groupby(level="plates")

    with PdfPages(outName) as pdf:
        for (name1, df1), (name2, df2) in zip(compDfgroup, noCompDfgroup):
            # print(name1, name2)
            numRows = 1 if name2 is None else 2
            fig, ax = plt.subplots(
                nrows=numRows, ncols=len(controlList), figsize=(10, 6)
            )
            for row in range(numRows):
                df = df1 if row == 0 else df2
                for i, control in enumerate(controlList):
                    subDf = df[
                        df.index.get_level_values(renameCol).str.contains(
                            f"{control}{sep}"
                        )
                    ]
                    titleName, correlations = calcCorreplations(
                        name=f"{control} in {name1 if row == 0 else name2}", df=subDf
                    )
                    activityScores = calculateScore(df=subDf)
                    passingScores = (
                        (activityScores >= threshold).sum() / len(activityScores) * 100
                    )

                    if len(controlList) == 1:
                        axis = ax
                    else:
                        axis = ax[i] if numRows == 1 else ax[(row, i)]
                    plotCorrs(
                        corrs=correlations,
                        title=f"{titleName}\n{passingScores:0.1f}% of {control} Controls >= {threshold} Activity Score",
                        ax=axis,
                    )
            fig.suptitle(f"{name1 if name2 is None else name2}")
            fig.tight_layout()
            pdf.savefig(fig, dpi=320)
            plt.close(fig=fig)
    return None


def generateControlsAboveThresh(
    inDF: pd.DataFrame,
    datasetLab: str,
    key: pd.DataFrame,
    controlList: list,
    threshold=0.5,
    **kwargs,
):
    inDF = parsePlates(inDf=inDF, **kwargs)
    plateResults = []
    controlLabels = [i.split("._.")[0] for i in controlList]

    for name, df in inDF.groupby(level="plates"):
        df = renameKeys(
            mainDf=df, keyDf=key, renameColumn="longname_proper", left_on="Wells"
        )
        df = calculateScore(df=df)

        percentages = []
        for control in controlList:
            controlDf = df[df.index.str.contains(control, na=False)]
            controlPercentage = ((controlDf >= threshold).sum() / len(controlDf)) * 100
            percentages.append(controlPercentage)

        results = pd.DataFrame(
            dict(
                {
                    "plate": [name for _ in range(len(controlList))],
                    "percentage": percentages,
                    "controlType": [control for control in controlList],
                }
            )
        )

        plateResults.append(results)

    plates = pd.concat(plateResults, axis=0)
    plates.reset_index(inplace=True, drop=True)

    colors = {"DMSO": "purple", "PMA": "limegreen"}

    fig, ax = plt.subplots(figsize=(16, 9))
    sns.barplot(
        data=plates, x="plate", y="percentage", hue="controlType", palette=colors, ax=ax
    )
    ax.set_xticklabels(
        ax.get_xticklabels(), rotation=45, size=12, ha="right", rotation_mode="anchor"
    )

    for p in ax.patches:
        height = p.get_height()
        ax.annotate(
            f"{height:0.1f}%",
            (p.get_x() + p.get_width() / 2.0, height),
            ha="center",
            va="bottom",
            fontsize=8,
        )

    ax.set_title(
        f"Percent of CP scores over {threshold} per control for {datasetLab}",
        fontsize=16,
    )
    fig.tight_layout()
    return fig
