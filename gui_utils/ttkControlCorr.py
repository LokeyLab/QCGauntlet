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
from modules import controlCorrsV2 as corr


class controlCorrelations(ttk.Frame):
    def __init__(self, parent, cursor, *args, **kwargs):
        super().__init__(parent)
        self.cond1, self.cond2, self.kwargs = None, None, None
        self.cursor = cursor

        self.topGrid = ttk.Frame(self, borderwidth=2, relief=SOLID)

        self.menu = controlCorrMenu(master=self.topGrid, borderwidth=2, relief=SOLID)
        self.runButton = ttk.Button(
            master=self.menu,
            text="View Figures",
            cursor=self.cursor,
            command=self.runBackend,
            width=10,
        )
        self.runButton.pack(side=TOP, padx=5, pady=10)
        self.menu.pack(side=LEFT, expand=False, padx=10, pady=5)

    def loadData(self, cond1: pd.DataFrame, cond2: pd.DataFrame = None, **kwargs):
        self.topGrid.pack_forget()

        self.cond1 = cond1
        self.cond2 = cond2
        self.kwargs = kwargs

        if cond2 is not None:
            self.cond2.index.name = "Wells"

        self.topGrid.pack(side=TOP, expand=False, fill=tk.X)

    def runBackend(self):
        sep, plateIndex = self.menu.getMenuOptions()


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
