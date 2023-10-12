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


class controlCorrelations(ttk.Frame):
    def __init__(self, parent, cursor, *args, **kwargs):
        super().__init__(parent)
        self.cursor = cursor

        self.topGrid = ttk.Frame(self, borderwidth=2, relief=SOLID)

        self.menu = controlCorrMenu(master=self.topGrid, borderwidth=2, relief=SOLID)
        self.menu.pack(side=LEFT, fill=X, expand=False, padx=10, pady=5)

        self.topGrid.pack(side=TOP, expand=False, fill=tk.X)

    def menu(self, parent=None):
        mainMenuframe = ttk.Frame(
            master=self if parent is None else parent, borderwidth=2, relief=SOLID
        )


class controlCorrMenu(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.menuLab = ttk.Label(
            self, anchor="center", width=20, text="Menu", font=("arial", 15, "bold")
        )
        self.menuLab.pack(side=TOP, fill=X, expand=True, padx=5, pady=10)

        self.sep = self.__buttonTextCombo(
            parent=self, preInsert="._.", text="String Separator"
        )
        self.sep.pack(side=TOP, anchor=CENTER)

        self.plateLabelIndex = self.__buttonTextCombo(
            parent=self, preInsert="-1", text="Plate ID Index"
        )
        self.plateLabelIndex.pack(side=TOP, anchor=CENTER)

    def __buttonTextCombo(self, parent, text, preInsert: str = None):
        mainFrame = tk.Frame(master=parent)

        self.entry = ttk.Entry(master=mainFrame, width=10)
        if preInsert is not None:
            self.entry.insert(0, preInsert)
        self.entry.pack(side=LEFT, anchor="w", padx=5, pady=5)

        self.text = ttk.Label(
            master=mainFrame, width=15, text=text, font=("arial", 12), anchor="center"
        )
        self.text.pack(side=RIGHT, anchor="e", padx=5, pady=10)
        return mainFrame
