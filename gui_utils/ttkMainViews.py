import tkinter as tk
from tkinter import ttk, filedialog
from ttkbootstrap import Style
import pandas as pd, numpy as np
import os

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

        self.menu()
        self.options = self.getMenuOptions
        self.cond1, self.cond2 = None, None
        self.kwargs = None

    def menu(self):
        self.menuOptions = ttk.Frame(
            master=self, borderwidth=2, relief=tk.SOLID, width=30
        )
        # self.menuOptions.pack(side=tk.TOP, anchor="nw", expand=True)
        self.menuOptions.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

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
        return self.sepEntry.get(), self.plateIndexEntry.get()

    def loadData(self, cond1: pd.DataFrame, cond2: pd.DataFrame = None, **kwargs):
        self.cond1, self.cond2 = cond1, cond2
        self.cond1.index.name = "Wells"
        self.cond2.index.name = "Wells"
        self.kwargs = kwargs

    def runBackend(self):
        # THIS WORKS NOW
        ds = cpa.createDataScores(compDf=self.cond1, noCompDf=self.cond2, **self.kwargs)
        return ds

    def hide(self):
        self.grid_forget()


class Yer(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)

        self.lab = ttk.Label(master=self, text="hey")
        self.lab.grid(row=10, column=0)
