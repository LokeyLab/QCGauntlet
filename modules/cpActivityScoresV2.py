import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
import os, subprocess, shutil, sys
from matplotlib.backends.backend_pdf import PdfPages
from modules import *


def getPlateActivityScores(
    compoundDf: pd.DataFrame,
    noCompDf: pd.DataFrame = None,
    map=None,
    activityTitles=["pma_ActivityScores", "noPma_ActivtyScores"],
    controlTitle=["DMSO", "PMA"],
    sep="._.",
    wellLabels="Wells",
    renameColumn="longname_proper",
    **kwargs,
):
    wells = [
        str(i).split("._.")[0]
        for i in list(compoundDf.index.get_level_values(wellLabels))
    ]

    try:
        plateName = list(noCompDf.index.get_level_values("plates"))
    except AttributeError:
        plateName = list(compoundDf.index.get_level_values("plates"))

    if noCompDf is None:
        plateComp = calculateScore(df=compoundDf.copy())
        rawData = {
            activityTitles[0]: plateComp.to_numpy(),
            "plate": plateName,
            "wells": wells,
        }
    else:
        plateComp = calculateScore(df=compoundDf.copy())
        plateNoCompDf = calculateScore(df=noCompDf.copy())
        rawData = {
            activityTitles[0]: plateComp.to_numpy(),
            activityTitles[1]: plateNoCompDf.to_numpy(),
            "plate": plateName,
            "wells": wells,
        }

    acScoreDf = pd.DataFrame(rawData)
    acScoreDf.sort_index(inplace=True)

    if map is not None:
        namingDf = compoundDf if noCompDf is None else noCompDf
        renamedDf = renameKeys(
            mainDf=namingDf, keyDf=map, renameColumn=renameColumn, left_on=wellLabels
        )
        acScoreDf["Full Proper Name"] = list(renamedDf.index)
        acScoreDf.set_index("Full Proper Name", inplace=True)
    else:
        acScoreDf["Full Proper Name"] = (
            list(compoundDf.index.get_level_values(wellLabels))
            if noCompDf is None
            else list(noCompDf.index.get_level_values(wellLabels))
        )
        acScoreDf.set_index("Full Proper Name", inplace=True)
    inclSep = lambda x: "".join([x, sep])
    wellType = [
        f"CONTROL_{controlTitle[0]}"
        if inclSep(controlTitle[0]) in i
        else f"CONTROL_{controlTitle[1]}"
        if len(controlTitle) > 1 and inclSep(controlTitle[1]) in i
        else "EXPERIMENTAL"
        for i in list(acScoreDf.index)
    ]
    acScoreDf["well_type"] = wellType

    return acScoreDf


def createDataScores(compDf: pd.DataFrame, noCompDf: pd.DataFrame = None, **kwargs):
    acScores = []
    sep = kwargs.get("sep", "._.")
    compDf = parsePlates(inDf=compDf, **kwargs)

    if noCompDf is not None:
        noCompDf = parsePlates(inDf=noCompDf, **kwargs)
        for (compName, currCompDf), (noCompName, currNoCompDf) in zip(
            compDf.groupby(level="plates"), noCompDf.groupby(level="plates")
        ):
            acScores.append(
                getPlateActivityScores(
                    compoundDf=currCompDf, noCompDf=currNoCompDf, **kwargs
                )
            )
    else:
        for compName, currCompDf in compDf.groupby(level="plates"):
            acScores.append(
                getPlateActivityScores(
                    compoundDf=currCompDf, noCompDf=noCompDf, **kwargs
                )
            )
    return pd.concat(acScores, axis=0)


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
    uniqueControls = ds["well_type"].unique()
    if hue is not None:
        colormap = plt.cm.get_cmap("tab10")
        colors = [colormap(i) for i in range(1, len(uniqueControls) + 1)]
        palette = {
            f"{control}": color for control, color in zip(uniqueControls, colors)
        }
        palette["EXPERIMENTAL"] = "C0"

    markers = [
        ",",
        "v",
        "^",
        "<",
        ">",
        "1",
        "2",
        "3",
        "4",
        "8",
        "s",
        "p",
        "*",
        "h",
        "H",
        "+",
        "x",
        "d",
        "|",
        "_",
        ".",
    ]
    markers = {f"{uniqueControls[i]}": markers[i] for i in range(len(uniqueControls))}
    markers["EXPERIMENTAL"] = "o"

    g = sns.FacetGrid(
        ds,
        col=groupByCol,
        col_wrap=col_wrap,
        hue=hue,
        palette=palette,
    )

    def plot_with_markers(data, x, y, **kwargs):
        ax = plt.gca()
        for control_type, marker in markers.items():
            data_subset = data[data["well_type"] == control_type]
            sns.scatterplot(
                data=data_subset,
                x=x,
                y=y,
                # color=palette.get(f"CONTROL_{control_type}", "C0"),
                marker=marker,
                alpha=0.75,
                ax=ax,
                **kwargs,
            )

    g.map_dataframe(plot_with_markers, x=x, y=y)
    # g.map_dataframe(
    #     func=snsPlot,
    #     x=x,
    #     y=y,
    #     alpha=0.75,
    # )

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
    pdfOut=True,
):
    groups = ds.groupby(groupByCol)

    figs = []
    for (
        name,
        df,
    ) in groups:
        fig, ax = plt.subplots(
            nrows=1, ncols=3, figsize=(3 * 4, 4)
        )  # make subplots of 1 row, 3 cols and then the next 2 cols are the elbow plots (sorted CP score)

        # control formatting
        uniqueCntrls = df["well_type"].unique()
        colormap = plt.cm.get_cmap("tab10")
        colors = [colormap(i) for i in range(1, len(uniqueCntrls) + 1)]
        controlColors = {
            f"{uniqueCntrls[i]}": colors[i] for i in range(len(uniqueCntrls))
        }
        controlColors["EXPERIMENTAL"] = "C0"

        colors = [controlColors.get(i, "C0") for i in df["well_type"].to_list()]

        # marker formatting
        markers = [
            ",",
            "v",
            "^",
            "<",
            ">",
            "1",
            "2",
            "3",
            "4",
            "8",
            "s",
            "p",
            "*",
            "h",
            "H",
            "+",
            "x",
            "d",
            "|",
            "_",
            ".",
        ]

        control_markers = {
            f"{uniqueCntrls[i]}": markers[i] for i in range(len(uniqueCntrls))
        }
        control_markers["EXPERIMENTAL"] = "o"

        scatter = sns.scatterplot(
            data=df,
            x=xCol,
            y=yCol,
            ax=ax[0],
            hue="well_type",
            palette=controlColors,
            style="well_type",
            markers=control_markers,
        )
        ax[0].axvline(x=threshold, color="r", zorder=2)
        ax[0].axhline(y=threshold, color="r", zorder=2)

        legend = ax[0].legend(
            loc="upper left", fontsize="small"
        )  # Position and size adjustments
        scatter.set_label("_nolegend_")

        # if control is not None:
        #     newDf = df[~(df.index.str.contains("|".join(control)))]
        # else:
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
        figs.append(fig)

    if pdfOut:
        with PdfPages(outname) as pdf:
            for fig in figs:
                pdf.savefig(figure=fig, dpi=320)
                plt.close(fig=fig)

    return figs


def genIndivElbows(
    ds: pd.DataFrame,
    groupByCol,
    yCol,
    outname,
    threshold=0.5,
    control=["DMSO", "PMA"],
    sep="._.",
    pdfOut=True,
):
    groups = ds.groupby(groupByCol)
    figs = []

    for name, df in groups:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 4))

        controlNames = [f"{control[i]}{sep}" for i in range(len(control))]
        newDf = df
        if control is not None:
            newDf = df[~(df.index.str.contains("|".join(controlNames)))]

        scores = newDf[yCol].sort_values().values
        x = [i for i in range(len(scores))]

        ax.plot(x, scores, linestyle="-", color="blue")
        ax.axhline(y=threshold, color="r", zorder=2)
        ax.set_xlabel("Compounds")
        ax.set_ylabel(yCol)
        ax.set_title(f"plate: {name} elbow plot")

        fig.tight_layout()
        figs.append(fig)

    if pdfOut:
        with PdfPages(outname) as pdf:
            for fig in figs:
                pdf.savefig(figure=fig, dpi=320)
                plt.close(fig=fig)

    return figs


def analyzeDf(
    dataset: pd.DataFrame, compLabel, outName, threshold=0.5, noCompLabel=None
):
    fullActivityScores = dataset.copy()
    with pd.ExcelWriter(outName, engine="xlsxwriter") as writer:
        fullActivityScores.to_excel(writer, sheet_name="All ActivityScores")

        if noCompLabel is not None:
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
        else:
            active = fullActivityScores[(fullActivityScores[compLabel] >= threshold)]
            active.to_excel(writer, sheet_name=f"scores >= {threshold}")

            notActive = fullActivityScores[(fullActivityScores[compLabel] < threshold)]
            notActive.to_excel(writer, sheet_name=f"scores < {threshold}")
