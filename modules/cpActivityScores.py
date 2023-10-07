import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
import os, subprocess, shutil, sys


def calculateScore(df: pd.DataFrame, axis):
    return df.apply(lambda x: np.sqrt(np.sum(np.square(x))), axis=axis)


def renameKeys(mainDf: pd.DataFrame, keyDf: pd.DataFrame, renameColumn) -> pd.DataFrame:
    mergeDf = pd.merge(
        mainDf, keyDf, left_index=True, right_index=True, how="left", sort=False
    ).copy()
    mergeDf.index = mergeDf[renameColumn]
    mergeDf = mergeDf.drop(renameColumn, axis=1, inplace=False)
    return mergeDf


def generatePlates(
    numPlates: int, excludeList=None, ds: str = "TargetMol", specPlates=None
):
    if specPlates is None:
        nums = [i for i in range(1, numPlates + 1)]
    else:
        nums = specPlates

    if excludeList is not None:
        nums = set(nums) - set(excludeList)

    return [f"{ds}_{str(i).zfill(2)}" for i in nums]


def getPlateActivityScores(
    plate,
    compoundDf: pd.DataFrame,
    noCompoundDf: pd.DataFrame,
    map=None,
    activityTitles=["pma_ActivityScores", "noPma_ActivtyScores"],
    controlTitles=["DMSO", "PMA"],
):
    if type(plate) is list:
        subsetComp = calculateScore(
            df=compoundDf[
                compoundDf.index.str.contains(plate[0])
                & compoundDf.index.str.contains(plate[1])
            ],
            axis=1,
        ).copy()
        subsetNoComp = calculateScore(
            df=noCompoundDf[
                noCompoundDf.index.str.contains(plate[0])
                & noCompoundDf.index.str.contains(plate[1])
            ],
            axis=1,
        ).copy()
    else:
        subsetComp = calculateScore(
            df=compoundDf[compoundDf.index.str.contains(plate)], axis=1
        ).copy()
        subsetNoComp = calculateScore(
            df=noCompoundDf[noCompoundDf.index.str.contains(plate)], axis=1
        ).copy()

    subsetComp.name = "activity score"
    subsetNoComp.name = "activity score"

    wells = [i.split("._.")[0] for i in list(subsetNoComp.index)]
    plateName = (
        ["".join(plate) for _ in range(subsetComp.shape[0])]
        if type(plate) is list
        else [plate for _ in range(subsetComp.shape[0])]
    )

    rawData = {
        activityTitles[0]: subsetComp.to_numpy(),
        activityTitles[1]: subsetNoComp.to_numpy(),
        "plate": plateName,
        "wells": wells,
    }

    acScoreDf = pd.DataFrame(rawData, index=wells)
    acScoreDf.sort_index(inplace=True)
    if map is not None:
        renamedDf = renameKeys(subsetNoComp, keyDf=map, renameColumn="longname_proper")
        acScoreDf["Full Proper Name"] = list(renamedDf.index)
        acScoreDf.set_index("Full Proper Name", inplace=True)

    wellType = [
        f"CONTROL_{controlTitles[0]}"
        if controlTitles[0] in i
        else f"CONTROL_{controlTitles[1]}"
        if controlTitles[1] in i
        else "EXPERIMENTAL"
        for i in list(acScoreDf.index)
    ]
    acScoreDf["well_type"] = wellType

    return acScoreDf


def createDataScores(
    numPlates: int,
    ds,
    compDf: pd.DataFrame,
    noCompDf: pd.DataFrame,
    map,
    activityTitles: list,
    specPlates=None,
    repList: list = None,
):
    plates = generatePlates(
        numPlates=numPlates, excludeList=repList, ds=ds, specPlates=specPlates
    )
    activityScores = [
        getPlateActivityScores(
            plate=plate,
            compoundDf=compDf,
            noCompoundDf=noCompDf,
            map=map,
            activityTitles=activityTitles,
        )
        for plate in plates
    ]

    if repList is not None:
        reps = [f"{ds}_{str(i).zfill(2)}" for i in repList]
        for plate in reps:
            for rep in ["_rep1", "_rep2"]:  # change this in the future
                activityScores.append(
                    getPlateActivityScores(
                        plate=[plate, rep],
                        compoundDf=compDf,
                        noCompoundDf=noCompDf,
                        map=map,
                        activityTitles=activityTitles,
                    )
                )

    return pd.concat(activityScores, axis=0, copy=True)


def createMultiPlot(
    ds,
    groupByCol,
    x,
    y,
    col_wrap=5,
    snsPlot=sns.scatterplot,
    threshold=0.5,
    hue=None,
    controlTitles=["DMSO", "PMA"],
):
    palette = None
    if hue is not None:
        palette = {
            f"CONTROL_{controlTitles[0]}": "purple",
            f"CONTROL_{controlTitles[1]}": "green",
            "EXPERIMENTAL": "C0",
        }

    g = sns.FacetGrid(ds, col=groupByCol, col_wrap=col_wrap, hue=hue, palette=palette)
    g.map_dataframe(func=snsPlot, x=x, y=y, alpha=0.75)

    for ax in g.axes.flat:
        ax.axvline(x=threshold, color="r", zorder=2)
        ax.axhline(y=threshold, color="r", zorder=2)
    return g


def genIndviPlots(
    ds: pd.DataFrame,
    groupByCol,
    xCol,
    yCol,
    outname,
    threshold=0.5,
    control=["DMSO", "PMA"],
):
    from matplotlib.backends.backend_pdf import PdfPages

    groups = ds.groupby(groupByCol)

    with PdfPages(outname) as p:
        for (
            name,
            df,
        ) in groups:
            fig, ax = plt.subplots(
                nrows=1, ncols=3, figsize=(3 * 4, 4)
            )  # make subplots of 1 row, 3 cols and then the next 2 cols are the elbow plots (sorted CP score)

            colors = [
                "purple"
                if i == f"CONTROL_{control[0]}"
                else "green"
                if i == f"CONTROL_{control[1]}"
                else "C0"
                for i in df["well_type"].to_list()
            ]
            df.plot.scatter(
                x=xCol,
                y=yCol,
                ax=ax[0],
                title=f"plate: {name} scatter plot",
                c=colors,
                alpha=0.75,
            )
            ax[0].axvline(x=threshold, color="r", zorder=2)
            ax[0].axhline(y=threshold, color="r", zorder=2)

            if control is not None:
                newDf = df[~(df.index.str.contains("|".join(control)))]
            else:
                newDf = df

            compScore = newDf[xCol].sort_values().values
            noCompScore = newDf[yCol].sort_values().values

            x = [i for i in range(len(compScore))]

            ax[1].plot(x, compScore, linestyle="-", color="blue")
            ax[1].axhline(y=threshold, color="r", zorder=2)
            ax[1].set_xlabel("Compounds")
            ax[1].set_ylabel(xCol)
            ax[1].set_title(f"plate: {name} elbow plot")

            ax[2].plot(x, noCompScore, linestyle="-", color="blue")
            ax[2].axhline(y=threshold, color="r", zorder=2)
            ax[2].set_xlabel("Compounds")
            ax[2].set_ylabel(yCol)
            ax[2].set_title(f"plate: {name} elbow plot")

            fig.tight_layout()
            fig.savefig(p, format="pdf", dpi=320)


def analyzeDf(dataset: pd.DataFrame, compLabel, noCompLabel, outName, threshold=0.5):
    fullActivityScores = dataset.copy()
    with pd.ExcelWriter(outName, engine="xlsxwriter") as writer:
        fullActivityScores.to_excel(writer, sheet_name="All ActivityScores")

        noActivityInBoth = fullActivityScores[
            (fullActivityScores[compLabel] < threshold)
            & (fullActivityScores[noCompLabel] < threshold)
        ].copy()
        noActivityInBoth.to_excel(
            writer, sheet_name=f"PMA and noPMA (both < {threshold})"
        )

        activityInBoth = fullActivityScores[
            (fullActivityScores[compLabel] >= threshold)
            & (fullActivityScores[noCompLabel] >= threshold)
        ].copy()
        activityInBoth.to_excel(
            writer, sheet_name=f"PMA and noPMA (both >= {threshold})"
        )

        activityInCompoundsVsnoCompounds = fullActivityScores[
            (fullActivityScores[compLabel] >= threshold)
            & (fullActivityScores[noCompLabel] < threshold)
        ].copy()
        activityInCompoundsVsnoCompounds.to_excel(
            writer, sheet_name=f"PMA>={threshold}; noPMA<{threshold}"
        )

        activityInNoCompoundsVsCompounds = fullActivityScores[
            (fullActivityScores[compLabel] < threshold)
            & (fullActivityScores[noCompLabel] >= threshold)
        ].copy()
        activityInNoCompoundsVsCompounds.to_excel(
            writer, sheet_name=f"PMA<{threshold}; noPMA>={threshold}"
        )
