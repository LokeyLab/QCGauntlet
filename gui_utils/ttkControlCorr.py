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

        lab = ttk.Label(master=self.topGrid, text="helloworld!")
        lab.pack(side=TOP, expand=True, fill=X)

        self.topGrid.pack(side=TOP)
