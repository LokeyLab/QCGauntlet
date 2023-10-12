import tkinter as tk
from tkinter import filedialog
from ttkbootstrap import Style, ttk
from ttkbootstrap.scrolled import ScrolledFrame
import pandas as pd, numpy as np
import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backends.backend_pdf import PdfPages

from gui_utils import *
from modules import cpActivityScoresV2 as cpa


class CPActivityScores(ttk.Frame):
    """
    CLI REFERENCE:
    options:
        -h, --help            show this help message and exit
        -s [SEP], --sep [SEP]
                                Determines the seperator/delimiter used to " "split text into their plates (default: "._.")
        -pi [PLATELABELINDEX], --plateLabelIndex [PLATELABELINDEX]
                                After seprating the index labels by the sep command, what index are the plate labels on? (def: -1)
        -at ACTIVITYTITLES [ACTIVITYTITLES ...], --activityTitles ACTIVITYTITLES [ACTIVITYTITLES ...]
                                titles of scores calculated in order of -c then -ac params (if -ac is used)
        -ct CONTROLTITLES [CONTROLTITLES ...], --controlTitles CONTROLTITLES [CONTROLTITLES ...]
                                List of control titles/labels (i.e. DMSO PMA)
    """

    def __init__(self, parent, cursor, **kwargs):
        super().__init__(parent)
        self.cursor = cursor

        self.options = self.getMenuOptions
        self.cond1, self.cond2 = None, None
        self.kwargs = None
        self.ds = None
        self.scatter = False

        self.topGrid = ttk.Frame(master=self, borderwidth=2, relief=tk.SOLID)
        self.nextGrid = ttk.Frame(master=self)

        self.menu(master=self.topGrid)

        self.topGrid.pack(side=tk.TOP, fill=tk.X, expand=False)
        self.nextGrid.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def menu(self, master=None):
        self.menuOptions = ttk.Frame(
            master=master if master is not None else self,
            borderwidth=2,
            relief=tk.SOLID,
            width=30,
        )
        self.menuOptions.pack(side=tk.LEFT, anchor="center", padx=10, pady=5)

        self.mentTitle = ttk.Label(
            master=self.menuOptions, text="Menu", width=20, font=("arial", 15, "bold")
        )
        self.mentTitle.configure(anchor=tk.CENTER)
        self.mentTitle.grid(row=0, column=0, columnspan=10, padx=5, pady=5)

        self.sepEntry = ttk.Entry(master=self.menuOptions, width=10)
        self.sepEntry.insert(0, "._.")
        self.sepEntry.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.sepEntryLabel = ttk.Label(
            master=self.menuOptions,
            width=15,
            text="String Seperator",
            font=("arial", 12),
        )
        self.sepEntryLabel.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        self.plateIndexEntry = ttk.Entry(master=self.menuOptions, width=10)
        self.plateIndexEntry.insert(0, "-1")
        self.plateIndexEntry.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.plateIndexEntryLabel = ttk.Label(
            master=self.menuOptions,
            width=15,
            text="Plate ID index",
            font=("arial", 12),
        )
        self.plateIndexEntryLabel.grid(row=2, column=1, padx=5, pady=5, sticky="e")

        self.generateButton = ttk.Button(
            master=self.menuOptions,
            text="View Figures",
            cursor=self.cursor,
            command=self.runBackend,
        )
        self.generateButton.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def getMenuOptions(self):
        return [self.sepEntry.get(), self.plateIndexEntry.get()]

    def loadData(self, cond1: pd.DataFrame, cond2: pd.DataFrame = None, **kwargs):
        self.cond1, self.cond2 = cond1, cond2
        self.cond1.index.name = "Wells"

        if cond2 is not None:
            self.cond2.index.name = "Wells"
            self.scatter = True
        else:
            self.scatter = False

        self.kwargs = kwargs

    def resetWidgets(self):
        self.menuOptions.pack_forget()

        try:
            self.dlOpts.pack_forget()
            self.changeView.pack_forget()
            self.activeFig.pack_forget()
        except:
            pass

        self.options = self.getMenuOptions
        self.cond1, self.cond2 = None, None
        self.kwargs = None
        self.ds = None

    def showWidgets(self):
        self.menuOptions.pack(side=tk.LEFT, anchor="center", padx=10, pady=5)

    def runBackend(self):
        # THIS WORKS NOW
        options = self.getMenuOptions()
        self.kwargs.update({"sep": options[0], "plateLabelIndex": int(options[1])})
        self.ds = cpa.createDataScores(
            compDf=self.cond1, noCompDf=self.cond2, **self.kwargs
        )

        if self.cond2 is not None:
            self.g = cpa.createMultiPlot(
                ds=self.ds,
                groupByCol="plate",
                x=self.kwargs["activityTitles"][0],
                y=self.kwargs["activityTitles"][1],
                hue="well_type",
                controlTitles=self.kwargs["controlTitle"],
                threshold=self.kwargs["threshold"],
            )
            self.g.add_legend()
            self.figs = cpa.genIndviPlots(
                ds=self.ds,
                groupByCol="plate",
                xCol=self.kwargs["activityTitles"][0],
                yCol=self.kwargs["activityTitles"][1],
                threshold=self.kwargs["threshold"],
                control=self.kwargs["controlTitle"],
                pdfOut=False,
                outname="dummy.pdf",
            )
        else:
            self.figs = cpa.genIndivElbows(
                ds=self.ds,
                groupByCol="plate",
                yCol=self.kwargs["activityTitles"][0],
                threshold=self.kwargs["threshold"],
                control=self.kwargs["controlTitle"],
                pdfOut=False,
                outname="dummy.pdf",
            )

        # self.activeFig = self.displayFigure(fig=self.figs)
        try:  # if someone reruns the notebook again
            self.dlOpts.pack_forget()
            self.changeView.pack_forget()
        except:
            pass

        self.dlOpts = self.downloadOptions(master=self.topGrid)
        self.dlOpts.pack_forget()

        self.changeView = self.graphViewer(master=self.topGrid)
        self.changeView.pack_forget()

        self.activeFig = DisplayFigure(fig=self.figs, master=self.nextGrid)

        self.activeFig.pack(side=TOP, expand=True, fill=BOTH, anchor=CENTER)
        self.dlOpts.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.Y)
        self.changeView.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.Y)

        return self.ds

    def hide(self):
        self.grid_forget()

    def downloadOptions(self, master=None, scatter=True):
        downloadOptionsMasterFrame = ttk.Frame(
            master=self if master is None else master,
            borderwidth=2,
            relief=tk.SOLID,
            width=30,
        )
        downloadOptionsMasterFrame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.Y)

        downloadLabel = ttk.Label(
            master=downloadOptionsMasterFrame,
            text="Download Options",
            font=("arial", 15, "bold"),
            width=20,
        )
        downloadLabel.configure(anchor=tk.CENTER)
        downloadLabel.pack(side=tk.TOP, anchor="center", fill=tk.Y)

        self.individualPlotButton = ttk.Button(
            master=downloadOptionsMasterFrame,
            text="Individual Plots",
            width=15,
            command=lambda: self.downLoadHandler(type=".pdf", multi=True),
        )
        self.individualPlotButton.pack(side=tk.TOP, padx=10, pady=5)

        self.activityScoreSheetButton = ttk.Button(
            master=downloadOptionsMasterFrame,
            text="Activity Score Sheet",
            width=15,
            command=lambda: self.downLoadHandler(type=".xlsx"),
        )
        self.activityScoreSheetButton.pack(side=tk.TOP, padx=10, pady=5)

        if self.scatter:
            self.scatterPlotbutton = ttk.Button(
                master=downloadOptionsMasterFrame,
                text="Scatter Plots",
                width=15,
                command=lambda: self.downLoadHandler(type=".pdf", multi=False),
            )
            self.scatterPlotbutton.pack(side=tk.TOP, padx=10, pady=5)

        return downloadOptionsMasterFrame

    def downLoadHandler(self, type=".xlsx", multi=True):
        filePath = filedialog.asksaveasfilename(defaultextension=type)
        if type == ".xlsx":
            cpa.analyzeDf(
                dataset=self.ds,
                compLabel=self.kwargs["activityTitles"][0],
                noCompLabel=self.kwargs["activityTitles"][1],
                threshold=self.kwargs["threshold"],
                outName=filePath,
            )
        elif type == ".pdf" and multi:
            with PdfPages(filePath) as pdf:
                for fig in self.figs:
                    pdf.savefig(fig)
        elif type == ".pdf" and not multi:
            self.g.savefig(filePath, format="pdf", dpi=320)

    def graphViewer(self, master=None, scatter=True):
        if self.cond2 is None:
            scatter = False

        def changeViewFig(fig):
            if not isinstance(fig, list):
                fig = [fig]
            self.activeFig.pack_forget()
            self.activeFig = DisplayFigure(fig, master=self.nextGrid)
            self.activeFig.pack(side=TOP, expand=True, fill=BOTH, anchor=CENTER)

        graphViewMainFrame = ttk.Frame(
            master=self if master is None else master, borderwidth=2, relief=tk.SOLID
        )
        graphViewMainFrame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.Y)

        graphViewLabel = ttk.Label(
            master=graphViewMainFrame,
            text="Figure View",
            font=("arial", 15, "bold"),
            width=20,
        )
        graphViewLabel.configure(anchor="center")
        graphViewLabel.pack(side=tk.TOP, fill=tk.X, anchor=tk.CENTER, padx=10, pady=5)

        indivPlotButton = ttk.Button(
            master=graphViewMainFrame,
            text="View Individual Plots",
            width=15,
            command=lambda: changeViewFig(fig=self.figs),
        )
        indivPlotButton.pack(side=tk.TOP, padx=10, pady=5)

        if self.scatter:
            scattePlotButton = ttk.Button(
                master=graphViewMainFrame,
                text="View Scatter Plot",
                width=15,
                command=lambda: changeViewFig(fig=self.g.fig),
            )
            scattePlotButton.pack(side=tk.TOP, padx=10, pady=5)
        return graphViewMainFrame


class Yer(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)

        self.lab = ttk.Label(master=self, text="hey")
        self.lab.grid(row=10, column=0)
