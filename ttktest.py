import pandas as pd
import numpy as np
import sys

import tkinter as tk
from tkinter import filedialog
from ttkbootstrap import Style, ttk
from ttkbootstrap.constants import *
from gui_utils.ttkMainMenu import *
from gui_utils.ttkCpActivityScore import CPActivityScores
from gui_utils.ttkControlCorr import controlCorrelations

from gui_utils import *

import ttkbootstrap as ttk

import modules.cpActivityScoresV2 as cpa

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backends.backend_pdf import PdfPages


class App(tk.Tk):
    def __init__(
        self,
        dataset,
        figs=None,
    ):
        super().__init__()
        style = Style(theme="darkly")
        self.geometry("1280x720")
        self.cursors = "dot"
        self.bootstyle = SUCCESS

        self.topFrame = ttk.Frame(master=self, borderwidth=2, relief=SOLID)
        self.topFrame.pack(side=tk.TOP, fill=tk.X, expand=FALSE)

        self.testLab = ttk.Label(
            master=self.topFrame, text="hello world", font=("arial", 25, "bold")
        )
        self.testLab.pack_configure(anchor="center")
        self.testLab.pack(side=TOP)

        self.figs = cpa.genIndviPlots(
            ds=dataset,
            groupByCol="plate",
            xCol="pma_ActivityScores",
            yCol="noPma_ActivtyScores",
            outname="test.pdf",
            pdfOut=False,
        )
        self.disp = DisplayFigure(fig=self.figs)
        self.disp.pack(side=TOP, fill=BOTH, expand=True)


def main():
    TARGETMOL_LOCATION = "/Users/dterciano/Desktop/LokeyLabFiles/TargetMol"
    assert os.path.isdir(TARGETMOL_LOCATION)

    noPmaFileLoc = "Datasets/TargetMol_DMSO_histdiffpy_nometa_Concatenated.csv"
    pmaFileLoc = "Datasets/TargetMol_PMA_histdiffpy_nometa_Concatenated.csv"

    noPmaFile = os.path.join(TARGETMOL_LOCATION, noPmaFileLoc)
    pmaFile = os.path.join(TARGETMOL_LOCATION, pmaFileLoc)
    # choose one of the two annotation sheets

    # keyFile = "/mnt/d/LabFiles/L4000-Bioactive Compound Library-Beverley Rabbitts (KIT10006535)_MapCleaned3_KSready.csv"
    keyFile = "/Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Annotations/TargetMol_KSReady_updatedTargets.csv"

    assert (
        os.path.isfile(noPmaFile)
        and os.path.isfile(pmaFile)
        and os.path.isfile(keyFile)
    )

    pma = pd.read_csv(pmaFile, sep=",", index_col=0)
    pma.index.name = "Wells"
    pma.columns.name = "Features"

    noPma = pd.read_csv(noPmaFile, sep=",", index_col=0)
    noPma.index.name = "Wells"
    pma.columns.name = "Features"

    key = pd.read_csv(keyFile, sep=",", index_col=1)
    key = key.loc[:, "longname_proper"]

    plate28PMAFile = "/Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Datasets/TargetMol_28PMA_rep1_PMA_blockCalc_histdiffpy.csv"
    plate28NoPMAFile = "/Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Datasets/TargetMol_28_rep1_DMSO_blockCalc_histdiffpy.csv"

    plate28PMA = pd.read_csv(plate28PMAFile, index_col=0)
    plate28NoPMA = pd.read_csv(plate28NoPMAFile, index_col=0)

    removeWells = ["N16._.TargetMol_08PMA_rep1", "A20._.TargetMol_07PMA_rep1"]
    pmaDropped = pma[~pma.index.str.contains("|".join(removeWells))]
    pmaDropped.shape

    keyDf = key.to_frame(name="longname_proper")

    def changeName(row):
        if "_rep2" in row.name:
            return row["longname_proper"] + "_rep2"
        else:
            return row["longname_proper"]

    keyDf["longname_proper"] = keyDf.apply(lambda row: changeName(row), axis=1)
    # display(keyDf)

    res = cpa.createDataScores(compDf=pmaDropped, map=keyDf, noCompDf=noPma)
    app = App(dataset=res)
    app.mainloop()
    return figs


if __name__ == "__main__":
    figs = main()
    app = App(figs=figs)
    app.mainloop()
