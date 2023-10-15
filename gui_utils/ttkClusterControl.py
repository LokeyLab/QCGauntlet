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

        self.mainFrame = ttk.Frame(master=self, borderwidth=2, relief=SOLID)
        self.mainFrame.pack(side=TOP, anchor=CENTER, padx=10, pady=10)

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

        self.sep.pack(side=TOP, padx=5, pady=5)
        self.plateIndex.pack(side=TOP, padx=5, pady=5)
        self.checkFrame.pack(side=TOP, padx=5, pady=5)
        self.genButton.pack(side=TOP, padx=5, pady=10)

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
