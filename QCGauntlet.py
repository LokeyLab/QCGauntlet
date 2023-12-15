import os, sys, shutil, subprocess
import pandas as pd
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

from modules import *
import modules.cpActivityScoresV2 as cpa
import modules.controlClusters as cc
import modules.controlCorrsV2 as corr


class CommandLine:
    def __init__(self, inOpts=None):
        import argparse

        ### init parser ###
        self.parser = argparse.ArgumentParser(
            description="A CLI program that processes datasets and analyzes the quality of it.",
            prog="QCGauntlet.py",
            usage="python %(prog)s [command] [arg] [subparser] ...",
            add_help=True,
            prefix_chars="-",
        )

        #### add subparser ###
        self.subparser = self.parser.add_subparsers(
            title="Gauntlet Analysis", dest="subcommands"
        )

        self.parser.add_argument(
            "-c",
            "--mainCond",
            action="store",
            nargs="?",
            type=str,
            required=True,
            help="File location/path for the main condition or first condition of the dataset (must be a .csv file)",
        )
        self.parser.add_argument(
            "-ac",
            "--alternateCond",
            action="store",
            nargs="?",
            type=str,
            required=False,
            default=None,
            help="(optional) File location/path ofr the second/alternate condition of the dataset (must be a .csv file if used)",
        )
        self.parser.add_argument(
            "-o",
            "--output",
            nargs="?",
            action="store",
            required=True,
            type=str,
            help="A string title for the output files (file extensions will be automatically handled)",
        )
        self.parser.add_argument(
            "-t",
            "--threshold",
            nargs="?",
            required=False,
            type=float,
            default=0.5,
            help="Sets the threshold value for analysis. (default: 0.5)",
        )
        self.parser.add_argument(
            "-indCol",
            "--indexColumn",
            default=[0],
            nargs="+",
            required=False,
            type=int,
            action="store",
            help="Specifies what the index column is in all "
            "the datasets (annotation sheet/plate maps don't count)",
        )
        # self.parser.add_argument(
        #     "-wl",
        #     "--wellLabel",
        #     action="store",
        #     type=str,
        #     default="Wells",
        #     help="The index label of -c and -ac which is of the same name "
        #     "(note: It cannot be "
        #     "none as pandas has difficulty parsing un-named indexes)",
        # )

        ### key df ###

        self.parser.add_argument(
            "-k",
            "--keyFile",
            nargs="?",
            action="store",
            required=False,
            default=None,
            help="Input path/location of annotation "
            "sheet/plate map (optional)"
            "//Use this only if you want to rename the wells in the dataset"
            "\n[Warning: certain analytical tools may require that this parameter is used]",
        )

        self.parser.add_argument(
            "-rc",
            "--renameColumns",
            nargs=2,
            type=str,
            required=False,
            default=["unambiguous_name", "longname_proper"],
            help="If the -k parameter is used then it is highly "
            "recommended that you use this parameter"
            " which is in the order of column that specifies "
            "wells and then column of their renamed values",
        )

        ############ subparser commands ############

        #### cpactivity ####
        self.cpActivityScoreSubparser = self.subparser.add_parser(
            "cpactivity",
            help="Activates cp Activity Score analysis and generates",
            add_help=True,
            prefix_chars="-",
        )
        self.cpActivityScoreSubparser.add_argument(
            "-s",
            "--sep",
            default="._.",
            required=False,
            nargs="?",
            action="store",
            help='Determines the seperator/delimiter used to "\
                "split text into their plates (default: "._.")',
        )
        self.cpActivityScoreSubparser.add_argument(
            "-pi",
            "--plateLabelIndex",
            default=-1,
            required=False,
            nargs="?",
            type=int,
            action="store",
            help="After seprating the index labels by the sep command,"
            " what index are the plate labels on? (def: -1)",
        )
        self.cpActivityScoreSubparser.add_argument(
            "-at",
            "--activityTitles",
            nargs="+",
            required=False,
            action="store",
            type=str,
            help="titles of scores calculated in order of"
            " -c then -ac params (if -ac is used)",
        )
        self.cpActivityScoreSubparser.add_argument(
            "-ct",
            "--controlTitles",
            nargs="+",
            required=False,
            action="store",
            type=str,
            help="List of control titles/labels (i.e. DMSO PMA)",
        )

        self.cpActivityScoreSubparser.add_argument(
            "-co",
            "--controlsOnly",
            action="store_true",
            default=False,
            required=False,
            help="Excludes experimental data points in final figures and data",
        )

        ### controlCluster ###
        self.controlClusterSubparser = self.subparser.add_parser(
            "controlCluster",
            help="Activates clustermap generation of controls",
            add_help=True,
            prefix_chars="-",
        )

        self.controlClusterSubparser.add_argument(
            "-s",
            "--sep",
            action="store",
            type=str,
            default="._.",
            nargs="?",
            required=False,
            help='Determines the seperator/delimiter used to "\
                "split text into their plates (default: "._.")',
        )
        self.controlClusterSubparser.add_argument(
            "-r",
            "--rowCLuster",
            action="store_false",
            default=True,
            required=False,
            help="Toggles row clustering (default: True)",
        )
        self.controlClusterSubparser.add_argument(
            "-c",
            "--colCLuster",
            action="store_false",
            default=True,
            required=False,
            help="Toggles column clustering (default: True)",
        )
        self.controlClusterSubparser.add_argument(
            "-ct",
            "--controlTitles",
            nargs="+",
            required=False,
            action="store",
            type=str,
            help="List of control titles/labels (i.e. DMSO PMA)",
        )
        self.controlClusterSubparser.add_argument(
            "-pi",
            "--plateLabelIndex",
            default=-1,
            required=False,
            nargs="?",
            type=int,
            action="store",
            help="After seprating the index labels by the sep command,"
            " what index are the plate labels on? (def: -1)",
        )

        ### controlHist ###
        self.controlHistSubparser = self.subparser.add_parser(
            "cntrlHist",
            help="Activates histogram generation of the distribution of control correlations",
            add_help=True,
            prefix_chars="-",
        )

        self.controlHistSubparser.add_argument(
            "-ct",
            "--controlTitles",
            nargs="+",
            required=False,
            action="store",
            type=str,
            help="List of control titles/labels (i.e. DMSO PMA)",
        )

        self.controlHistSubparser.add_argument(
            "-pi",
            "--plateLabelIndex",
            default=-1,
            required=False,
            nargs="?",
            type=int,
            action="store",
            help="After seprating the index labels by the sep command,"
            " what index are the plate labels on? (def: -1)",
        )

        self.controlHistSubparser.add_argument(
            "-s",
            "--sep",
            action="store",
            type=str,
            default="._.",
            nargs="?",
            required=False,
            help='Determines the seperator/delimiter used to "\
                "split text into their plates (default: "._.")',
        )

        ### control Barplots ###
        self.controlBarplotsSubparser = self.subparser.add_parser(
            "cntrlBarPlots",
            help="Activates generation of controls over threshold in the form of barplots",
            add_help=True,
            prefix_chars="-",
        )
        self.controlBarplotsSubparser.add_argument(
            "-ds",
            "--datasetLabel",
            action="store",
            required=True,
            nargs="+",
            type=str,
            help="Specifies what to name figure from "
            "the dataset name (i.e. PMA plate)"
            " if 2 conditions are inputted, then the "
            "arguments could be: name for -c then name for -ac",
        )
        self.controlBarplotsSubparser.add_argument(
            "-ct",
            "--controlTitles",
            nargs="+",
            required=False,
            action="store",
            type=str,
            help="List of control titles/labels (i.e. DMSO PMA)",
        )
        self.controlBarplotsSubparser.add_argument(
            "-pi",
            "--plateLabelIndex",
            default=-1,
            required=False,
            nargs="?",
            type=int,
            action="store",
            help="After seprating the index labels by the sep command,"
            " what index are the plate labels on? (def: -1)",
        )

        self.controlBarplotsSubparser.add_argument(
            "-s",
            "--sep",
            action="store",
            type=str,
            default="._.",
            nargs="?",
            required=False,
            help='Determines the seperator/delimiter used to "\
                "split text into their plates (default: "._.")',
        )

        if inOpts is None:
            self.args = self.parser.parse_args()
        else:
            self.args = self.parser.parse_args(inOpts)


def main(inOpts=None):
    cl = CommandLine(inOpts=inOpts)
    cond1 = pd.read_csv(cl.args.mainCond, sep=",", index_col=cl.args.indexColumn)
    cond1.index.name = "wells"
    cond2 = None
    if cl.args.alternateCond is not None:
        cond2 = pd.read_csv(
            cl.args.alternateCond, sep=",", index_col=cl.args.indexColumn
        )
        cond2.index.name = "wells"

    key = cl.args.keyFile
    if key is not None:
        key = pd.read_csv(key)
        key = key[cl.args.renameColumns]
        key.set_index(cl.args.renameColumns[0], inplace=True)

    if cl.args.subcommands == "cpactivity":  # scatter plots
        # properties and config:
        # sep x
        # plateLabelIndex x
        # map -> sep function or subparser
        # activityTitles x
        # control Titles x
        # wellLabels x
        # renameColumn x
        if cond2 is not None and len(cl.args.activityTitles) == 1:
            print(
                "2 titles (-at flag) are needed in"
                " order to create the formatted dataset",
                file=sys.stderr,
            )
            exit(1)

        resDataset = cpa.createDataScores(
            compDf=cond1,
            noCompDf=cond2,
            sep=cl.args.sep,
            plateLabelIndex=cl.args.plateLabelIndex,
            activityTitles=cl.args.activityTitles,
            controlTitle=cl.args.controlTitles,
            # wellLabels=cl.args.wellLabel,
            wellLabels="wells",
            renameColumn=cl.args.renameColumns[1],
            map=key,
            expExclude=cl.args.controlsOnly,
        )

        cpa.analyzeDf(
            dataset=resDataset,
            compLabel=cl.args.activityTitles[0],
            threshold=cl.args.threshold,
            noCompLabel=cl.args.activityTitles[1] if cond2 is not None else None,
            outName=f"{cl.args.output}_activityScore.xlsx",
        )
        if cond2 is None:
            cpa.genIndivElbows(
                ds=resDataset,
                groupByCol="plate",
                yCol=cl.args.activityTitles[0],
                outname=f"{cl.args.output}_elboPlot.pdf",
                threshold=cl.args.threshold,
                control=cl.args.controlTitles,
                sep=cl.args.sep,
            )
        else:
            g = cpa.createMultiPlot(
                ds=resDataset,
                groupByCol="plate",
                x=cl.args.activityTitles[0],
                y=cl.args.activityTitles[1],
                threshold=cl.args.threshold,
                hue="well_type",
                controlTitles=cl.args.controlTitles,
            )
            g.add_legend()
            g.savefig(f"{cl.args.output}_multiPlot.pdf", format="pdf", dpi=320)

            cpa.genIndviPlots(
                ds=resDataset,
                groupByCol="plate",
                xCol=cl.args.activityTitles[0],
                yCol=cl.args.activityTitles[1],
                outname=f"{cl.args.output}_individualPlots.pdf",
                threshold=cl.args.threshold,
                control=cl.args.controlTitles,
            )
    elif cl.args.subcommands == "controlCluster":
        if key is None:
            print(
                "A key file/annotation sheet must be supplied! "
                "(use -k and -rc for the key file)",
                file=sys.stderr,
            )
            exit(1)
        formatDf = cc.formatDf(
            compDf=cond1,
            noCompDf=cond2,
            key=key,
            sep=cl.args.sep,
            controls=cl.args.controlTitles,
            renameColumn=cl.args.renameColumns[1],
            plateLabelIndex=cl.args.plateLabelIndex,
        )

        outname = f"{cl.args.output}_clusterMap"
        cc.genTreeViewClustMap(
            inDf=formatDf,
            outname=outname,
            rowCluster=cl.args.rowCLuster,
            colCluster=cl.args.colCLuster,
        )
    elif cl.args.subcommands == "cntrlHist":
        if key is None:
            print(
                "A key file/annotation sheet must be supplied! "
                "(use -k and -rc for the key file)",
                file=sys.stderr,
            )
            exit(1)
        outname = f"{cl.args.output}_cntrlHist.pdf"
        corr.generateControlCorrsAnalysis(
            compDf=cond1,
            noCompDf=cond2,
            key=key,
            controlList=cl.args.controlTitles,
            threshold=cl.args.threshold,
            sep=cl.args.sep,
            plateLabelIndex=cl.args.plateLabelIndex,
            outName=outname,
        )
    elif cl.args.subcommands == "cntrlBarPlots":
        if key is None:
            print(
                "A key file/annotation sheet must be supplied! "
                "(use -k and -rc for the key file)",
                file=sys.stderr,
            )
            exit(1)
        outname = f"{cl.args.output}_barPlots.pdf"
        with PdfPages(outname) as pdf:
            fig = corr.generateControlsAboveThresh(
                inDF=cond1,
                datasetLab=cl.args.datasetLabel[0],
                key=key,
                controlList=cl.args.controlTitles,
                threshold=cl.args.threshold,
                sep=cl.args.sep,
                plateLabelIndex=cl.args.plateLabelIndex,
            )
            pdf.savefig(figure=fig, dpi=320)
            plt.close(fig)

            if cond2 is not None:
                fig = corr.generateControlsAboveThresh(
                    inDF=cond2,
                    datasetLab=cl.args.datasetLabel[1],
                    key=key,
                    controlList=cl.args.controlTitles,
                    threshold=cl.args.threshold,
                    sep=cl.args.sep,
                    plateLabelIndex=cl.args.plateLabelIndex,
                )
                pdf.savefig(figure=fig, dpi=320)
                plt.close(fig)

    return


if __name__ == "__main__":
    main()
