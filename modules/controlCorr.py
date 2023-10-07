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


def calculateScore(df: pd.DataFrame, axis=1):
    return df.apply(lambda x: np.sqrt(np.sum(np.square(x))), axis=axis)


def renameKeys(
    mainDf: pd.DataFrame,
    keyDf: pd.DataFrame,
    renameColumn,
    left_index=True,
    left_on="Wells",
) -> pd.DataFrame:
    if left_index:
        mergeDf = pd.merge(
            mainDf, keyDf, left_index=True, right_index=True, how="left", sort=False
        ).copy()
    else:
        mergeDf = pd.merge(
            mainDf, keyDf, left_on=left_on, right_index=True, how="left", sort=False
        ).copy()
    mergeDf.index = mergeDf[renameColumn]
    mergeDf = mergeDf.drop(renameColumn, axis=1, inplace=False)
    return mergeDf


def sepControls(name: str, controlList: list, df: pd.DataFrame):
    control0 = df[df.index.str.contains(controlList[0], na=False)]  # i.e. PMA
    control1 = df[df.index.str.contains(controlList[1], na=False)]  # i.e. DMSO

    control0Name, control0Corrs = calcCorreplations(
        name=f"{controlList[0]} in {name}", df=control0
    )  # i.e. PMA
    control1Name, control1Corrs = calcCorreplations(
        name=f"{controlList[1]} in {name}", df=control1
    )  # i.e. DMSO

    control0Scores = calculateScore(df=control0, axis=1)
    control1Score = calculateScore(df=control1, axis=1)

    return (control0, control0Name, control0Corrs, control0Scores), (
        control1,
        control1Name,
        control1Corrs,
        control1Score,
    )


def generateControlCorrsAnalysis(
    compDf: pd.DataFrame,
    noCompDf: pd.DataFrame,
    groupbyCol: str,
    outName: str,
    key: pd.DataFrame,
    controlList=None,
    threshold=0.5,
):
    with PdfPages(outName) as pdf:
        for (compName, compDf), (noCompName, noCompDf) in zip(
            compDf.groupby(level=groupbyCol), noCompDf.groupby(level=groupbyCol)
        ):
            compDf = renameKeys(
                mainDf=compDf,
                keyDf=key,
                renameColumn="longname_proper",
                left_index=False,
                left_on="Wells",
            )
            noCompDf = renameKeys(
                mainDf=noCompDf,
                keyDf=key,
                renameColumn="longname_proper",
                left_index=False,
                left_on="Wells",
            )

            fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(10, 6))
            name = lambda x: "PMA plate" if "PMA" in x else "noPMA plate"
            controlNames = [i.split("._.")[0] for i in controlList]

            # COMPOUND PLATE ANALYSIS
            controls = sepControls(
                controlList=controlList, df=compDf, name=name(compName)
            )
            control0, control0Name, control0Corrs, control0Scores = controls[0]
            control1, control1Name, control1Corrs, control1Scores = controls[1]

            control0ScorePercent = (
                (control0Scores >= threshold).sum() / len(control0Scores)
            ) * 100
            control1ScorePercent = (
                (control1Scores >= threshold).sum() / len(control1Scores)
            ) * 100

            control0Name = "".join(control0Name.split("._."))
            control1Name = "".join(control1Name.split("._."))

            plotCorrs(
                corrs=control0Corrs,
                title=f"{control0Name}\n{control0ScorePercent:0.1f}% of {controlNames[0]} Controls >= {threshold} Activity Score",
                ax=ax[0][0],
            )
            plotCorrs(
                corrs=control1Corrs,
                title=f"{control1Name}\n{control1ScorePercent:0.1f}% of {controlNames[1]} Controls >= {threshold} Activity Score",
                ax=ax[0][1],
            )

            # NO COMPOUND PLATE ANALYSIS
            controls = sepControls(
                controlList=controlList, df=noCompDf, name=name(noCompName)
            )
            control0, control0Name, control0Corrs, control0Scores = controls[0]
            control1, control1Name, control1Corrs, control1Scores = controls[1]

            control0ScorePercent = (
                (control0Scores >= threshold).sum() / len(control0Scores)
            ) * 100
            control1ScorePercent = (
                (control1Scores >= threshold).sum() / len(control1Scores)
            ) * 100

            control0Name = "".join(control0Name.split("._."))
            control1Name = "".join(control1Name.split("._."))

            plotCorrs(
                corrs=control0Corrs,
                title=f"{control0Name}\n{control0ScorePercent:0.1f}% of {controlNames[0]} Controls >= {threshold} Activity Score",
                ax=ax[1][0],
            )
            plotCorrs(
                corrs=control1Corrs,
                title=f"{control1Name}\n{control1ScorePercent:0.1f}% of {controlNames[1]} Controls >= {threshold} Activity Score",
                ax=ax[1][1],
            )

            fig.suptitle(f"{noCompName} Control Correlations")

            fig.tight_layout()
            pdf.savefig(fig, dpi=320)
    return


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
            mainDf=df, keyDf=key, renameColumn="longname_proper", left_index=False
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
