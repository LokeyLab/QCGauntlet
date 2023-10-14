import tkinter as tk
from tkinter import filedialog
from ttkbootstrap import Style, ttk
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import filedialog
import pandas as pd, numpy as np
import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backends.backend_pdf import PdfPages

from gui_utils import *
from modules import controlCorrsV2 as corr


class ControlCorrelations(ttk.Frame):
    def __init__(self, parent, cursor, *args, **kwargs):
        super().__init__(parent)
        self.cond1, self.cond2, self.key, self.kwargs = None, None, None, None
        self.cursor = cursor
        self.corrFigs, self.barFigs = None, None
        self.defaultView = True

        ############### TOP GRID ###############
        self.topGrid = ttk.Frame(self, borderwidth=2, relief=SOLID)

        topGridLab = ttk.Label(
            master=self.topGrid,
            text="Correlations and Activities of Control Wells",
            font=("arial", 20, "bold"),
            anchor=CENTER,
        )
        topGridLab.pack(side=TOP, fill=X, padx=10, pady=1)
        sep = ttk.Separator(master=self.topGrid)
        sep.pack(side=TOP, fill=X, padx=1, pady=5)

        self.menu = controlCorrMenu(master=self.topGrid, borderwidth=2, relief=SOLID)
        self.runButton = ttk.Button(
            master=self.menu,
            text="View Figures",
            cursor=self.cursor,
            command=self.runBackend,
            width=10,
        )

        self.menu.pack(side=LEFT, expand=False, padx=10, pady=5)
        self.runButton.pack(side=TOP, padx=5, pady=5)

        self.dlMenu = DownloadMenu(
            master=self.topGrid, borderwidth=2, relief=SOLID, cursor=self.cursor
        )
        self.viewMenu = ViewMenu(
            cursor=self.cursor, master=self.topGrid, borderwidth=2, relief=SOLID
        )

        self.figView = ttk.Frame(self, borderwidth=2, relief=SOLID)
        ############### TEMP CODE ###############
        # self.dlMenu.pack(side=LEFT, fill=Y, padx=10, pady=5)  # ALSO DELETE THIS

        # self.viewMenu.pack(side=LEFT, fill=Y, padx=10, pady=5)  # DELETE THIS

        # self.topGrid.pack(side=TOP, expand=False, fill=tk.X)  # DELETE THIS
        # self.figView.pack(side=TOP, expand=TRUE, fill=BOTH)

    def __del__(self):
        if self.figs is not None:
            for fig in self.figs:
                plt.close(fig=fig)

    def hideAll(self):
        self.dlMenu.pack_forget()
        self.viewMenu.pack_forget()
        self.topGrid.pack_forget()
        self.figView.pack_forget()

        try:
            self.activeDisplay.pack_forget()
        except:
            pass

    def changeActiveDisp(self, figure):
        try:
            self.activeDisplay.pack_forget()
        except:
            pass

        self.activeDisplay = DisplayFigure(fig=figure, master=self.figView)
        self.activeDisplay.pack(side=TOP, fill=BOTH, expand=True)

    def loadData(self, cond1: pd.DataFrame, cond2: pd.DataFrame = None, **kwargs):
        self.hideAll()  # UNCOMMENT THIS FOR FINAL PRODUCT

        self.cond1 = cond1
        self.cond2 = cond2
        self.kwargs = kwargs

        if cond2 is not None:
            self.cond2.index.name = "Wells"

        self.topGrid.pack(side=TOP, expand=False, fill=tk.X)  # UNCOMMENT THIS

    def runBackend(self):
        self.viewMenu.pack_forget()
        self.dlMenu.pack_forget()
        try:
            self.activeDisplay.pack_forget()
        except:
            pass

        sep, plateIndex = self.menu.getMenuOptions()
        self.kwargs.update({"sep": sep, "plateLabelIndex": int(plateIndex)})

        self.corrFigs = corr.generateControlCorrsAnalysis(
            compDf=self.cond1,
            noCompDf=self.cond2,
            outName="dummy.pdf",
            pdfOut=False,
            **self.kwargs,
        )
        self.barFigs = [
            corr.generateControlsAboveThresh(
                inDF=self.cond1,
                datasetLab=self.kwargs["activityTitles"][0],
                renameCol="Wells",
                **self.kwargs,
            )
        ]
        if self.cond2 is not None:
            self.barFigs.append(
                corr.generateControlsAboveThresh(
                    inDF=self.cond2,
                    datasetLab=self.kwargs["activityTitles"][1],
                    renameCol="Wells",
                    **self.kwargs,
                )
            )

        # self.activeDisplay = DisplayFigure(fig=self.figs, master=self.figView)

        self.changeActiveDisp(figure=self.corrFigs)

        self.dlMenu.pack(side=LEFT, fill=Y, padx=10, pady=5)
        self.viewMenu.pack(side=LEFT, fill=Y, padx=10, pady=5)
        # self.activeDisplay.pack(side=TOP, fill=BOTH, expand=True)
        self.figView.pack(side=TOP, expand=TRUE, fill=BOTH)


class controlCorrMenu(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menuLab = ttk.Label(
            self, anchor="center", width=20, text="Menu", font=("arial", 15, "bold")
        )
        self.menuLab.pack(side=TOP, fill=X, expand=True, padx=5, pady=10)

        self.sep, self.sepReturn = self.__buttonTextCombo(
            parent=self, preInsert="._.", text="String Separator"
        )
        self.sep.pack(side=TOP, anchor=CENTER)

        self.plateLabelIndex, self.plateLabReturn = self.__buttonTextCombo(
            parent=self, preInsert="-1", text="Plate ID Index"
        )
        self.plateLabelIndex.pack(side=TOP, anchor=CENTER)

    def __buttonTextCombo(self, parent, text, preInsert: str = None):
        mainFrame = tk.Frame(master=parent)

        entry = ttk.Entry(master=mainFrame, width=10)
        if preInsert is not None:
            entry.insert(0, preInsert)
        entry.pack(side=LEFT, anchor="w", padx=5, pady=5)

        text = ttk.Label(
            master=mainFrame, width=15, text=text, font=("arial", 12), anchor="center"
        )
        text.pack(side=RIGHT, anchor="e", padx=5, pady=10)

        return mainFrame, entry

    def getMenuOptions(self):
        return self.sepReturn.get(), self.plateLabReturn.get()


class DownloadMenu(ttk.Frame):
    def __init__(self, cursor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cursor = cursor

        self.dlMenuLabel = ttk.Label(
            master=self,
            text="Download Options",
            width=20,
            font=("arial", 15, "bold"),
            anchor=CENTER,
        )
        self.dlMenuLabel.pack(
            side=TOP, fill=X, expand=False, padx=5, pady=10, anchor=CENTER
        )

        self.histDownloadButton = ttk.Button(
            master=self,
            text="Control Histograms",
            width=15,
            command=self.downloadHandler,
            cursor=self.cursor,
        )
        self.histDownloadButton.pack(side=TOP, padx=10, pady=5, anchor=CENTER)

        self.barDownloadButton = ttk.Button(
            master=self,
            text="Control Bar Plots",
            width=15,
            command=lambda: self.downloadHandler(hist=False),
            cursor=self.cursor,
        )
        self.barDownloadButton.pack(side=TOP, padx=10, pady=5, anchor=CENTER)

    def downloadHandler(self, hist=True):
        filePath = filedialog.asksaveasfilename(defaultextension=".pdf")

        with PdfPages(filePath) as pdf:
            if hist:
                figs = self.master.master.corrFigs
            else:
                figs = self.master.master.barFigs

            for fig in figs:
                pdf.savefig(fig, dpi=320)
                plt.close(fig=fig)

        return


class ViewMenu(ttk.Frame):
    def __init__(self, cursor, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cursor = cursor
        self.viewMenu = ttk.Label(
            master=self,
            text="Figure View",
            font=("arial", 15, "bold"),
            width=20,
            anchor=CENTER,
        )
        self.viewMenu.pack(side=TOP, fill=X, anchor=CENTER, padx=10, pady=10)

        self.histViewButton = ttk.Button(
            master=self,
            text="View Histograms",
            width="15",
            cursor=self.cursor,
            command=self.viewHandler,
        )
        self.histViewButton.pack(side=TOP, anchor=CENTER, padx=10, pady=5)

        self.barPlotViewButton = ttk.Button(
            master=self,
            text="View Bar Plots",
            width=15,
            cursor=self.cursor,
            command=lambda: self.viewHandler(defView=False),
        )
        self.barPlotViewButton.pack(side=TOP, anchor=CENTER, padx=10, pady=5)

    def viewHandler(self, defView=True):
        # access ControlCorrelations Class
        if defView:
            self.master.master.changeActiveDisp(self.master.master.corrFigs)
        else:
            self.master.master.changeActiveDisp(self.master.master.barFigs)
        return
