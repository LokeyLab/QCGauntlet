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
from modules import controlClusters as cc


class ControlClustering(ttk.Frame):
    def __init__(self, cursor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cursor = cursor
        self.cond1, self.cond2 = None, None
        self.key = None
        self.kwargs = None

        self.mainFrame = ttk.Frame(master=self, borderwidth=2, relief=SOLID)

        self.titleLabel = ttk.Label(
            master=self.mainFrame,
            anchor=CENTER,
            text="Control Clustermap File Generator",
            width=30,
            font=("arial", 25, "bold"),
        )
        self.titleLabel.pack(side=TOP, anchor=CENTER, padx=10, pady=10)

        self.genButton = ttk.Button(
            master=self.mainFrame,
            text="Generate files",
            width=20,
            cursor=self.cursor,
            command=self.runBackend,
        )

        self.sep, self.sepEntry = self.__buttonTextCombo(
            parent=self.mainFrame, text="Separator", preInsert="._."
        )
        self.plateIndex, self.plateIndexEntry = self.__buttonTextCombo(
            parent=self.mainFrame, text="Plate Index label", preInsert="-1"
        )

        self.checkFrame, self.rowClustVar, self.colClusterVar = self.__checkButtonCombo(
            parent=self.mainFrame, text1="Row Clustering", text2="Column Clustering"
        )

        self.notifLabel = ttk.Label(
            self,
            anchor=CENTER,
            text="Please be patient, Java TreeView File Generation may take a while",
            font=("arial", 30, "bold"),
            borderwidth=2,
            relief=SOLID,
        )

        self.sep.pack(side=TOP, padx=5, pady=5)
        self.plateIndex.pack(side=TOP, padx=5, pady=5)
        self.checkFrame.pack(side=TOP, padx=5, pady=5)
        self.genButton.pack(side=TOP, padx=5, pady=10)
        # self.mainFrame.pack(side=TOP, anchor=CENTER, padx=10, pady=10)

    def __buttonTextCombo(self, parent, text, preInsert: str = None):
        mainFrame = tk.Frame(master=parent)

        entry = ttk.Entry(master=mainFrame, width=10)
        if preInsert is not None:
            entry.insert(0, preInsert)
        entry.pack(side=LEFT, anchor="w", padx=5, pady=5)

        text = ttk.Label(
            master=mainFrame, width=15, text=text, font=("aria", 12), anchor="center"
        )
        text.pack(side=RIGHT, anchor="e", padx=5, pady=10)

        return mainFrame, entry

    def __checkButtonCombo(self, parent, text1, text2):
        mainFrame = tk.Frame(master=parent)
        rowClusterVar = tk.BooleanVar(value=True)
        colCLusterVar = tk.BooleanVar(value=True)

        rowClusterCheck = ttk.Checkbutton(
            master=mainFrame,
            style="info.Roundtoggle.Toolbutton",
            text="Row Clustering",
            width=15,
            variable=rowClusterVar,
        )
        rowClusterCheck.pack(side=TOP, padx=5, pady=10, anchor=CENTER)

        colClusterCheck = ttk.Checkbutton(
            master=mainFrame,
            style="info.Roundtoggle.Toolbutton",
            text="Column Clustering",
            width=15,
            variable=colCLusterVar,
            bootstyle=SUCCESS,
        )
        colClusterCheck.pack(side=TOP, anchor=CENTER, padx=5, pady=10)

        return mainFrame, rowClusterVar, colCLusterVar

    def loadData(
        self, cond1: pd.DataFrame, cond2: pd.DataFrame = None, key=None, **kwargs
    ):
        # self.mainFrame.pack_forget()

        self.cond1 = cond1
        self.cond2 = cond2
        self.key = key
        self.kwargs = kwargs

        self.cond1.index.name = "Wells"
        if self.cond2 is not None:
            self.cond2.index.name = "Wells"

        self.mainFrame.pack(side=TOP, anchor=CENTER, padx=10, pady=10)

    def runBackend(self):
        if self.key is None:
            tk.messagebox.showerror(
                title="Error",
                message="A key file must be inputted in order to use this function",
            )
            return
        self.notifLabel.pack(side=TOP, fill=tk.Y, expand=True, padx=10, pady=15)
        self.kwargs.update(
            {
                "rowCluster": self.rowClustVar.get(),
                "colCluster": self.colClusterVar.get(),
                "sep": self.sepEntry.get(),
                "plateLabelIndex": int(self.plateIndexEntry.get()),
            }
        )
        filePath = filedialog.asksaveasfilename()

        try:
            df = cc.formatDf(
                compDf=self.cond1, noCompDf=self.cond2, key=self.key, **self.kwargs
            )

            cc.genTreeViewClustMap(
                inDf=df,
                outname=filePath,
                rowCluster=self.kwargs["rowCluster"],
                colCluster=self.kwargs["colCluster"],
            )
        except Exception as e:
            tk.messagebox.showerror(title="Error", message=f"{type(e).__name__}: {e}")
            return
        self.notifLabel.pack_forget()
