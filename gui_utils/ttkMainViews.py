import tkinter as tk
from tkinter import filedialog
from ttkbootstrap import Style, ttk
from ttkbootstrap.scrolled import ScrolledFrame
import pandas as pd, numpy as np
import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

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
        self.menu()

        # self.grid_rowconfigure(1, weight=1)  # Allow vertical expansion
        # self.grid_columnconfigure(0, weight=1)

    def menu(self):
        self.menuOptions = ttk.Frame(
            master=self, borderwidth=2, relief=tk.SOLID, width=30
        )
        self.menuOptions.pack(side=tk.TOP, anchor="w")
        # self.menuOptions.pack(side=tk.TOP, anchor="nw", expand=True)
        # self.menuOptions.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

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
        self.cond2.index.name = "Wells"
        self.kwargs = kwargs

    def runBackend(self):
        # THIS WORKS NOW
        options = self.getMenuOptions()
        self.kwargs.update({"sep": options[0], "plateLabelIndex": int(options[1])})
        ds = cpa.createDataScores(compDf=self.cond1, noCompDf=self.cond2, **self.kwargs)
        self.ds = ds
        g = cpa.createMultiPlot(
            ds=self.ds,
            groupByCol="plate",
            x=self.kwargs["activityTitles"][0],
            y=self.kwargs["activityTitles"][1],
            hue="well_type",
            controlTitles=self.kwargs["controlTitle"],
        )
        self.displayFigure(fig=g.fig)

        return ds

    def displayFigure(self, fig):
        masterFrame = ttk.Frame(
            self,
            borderwidth=2,
            # padx=10,
            # pady=10,
            relief=tk.SOLID,
            # bg="#6562ff"
        )
        masterFrame.pack(side=tk.TOP, expand=True, fill=tk.BOTH, anchor=tk.CENTER)

        topGroupFrame = tk.Frame(master=masterFrame)
        canvas = tk.Canvas(master=topGroupFrame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        vScrollFrame = tk.Frame(master=topGroupFrame)
        vScroll = ttk.Scrollbar(
            master=vScrollFrame, orient=tk.VERTICAL, command=canvas.yview
        )
        vScroll.pack(side=tk.LEFT, expand=True, fill=tk.Y)
        vScrollFrame.pack(side=tk.LEFT, expand=False, fill=tk.Y)
        topGroupFrame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        hScrollFrame = tk.Frame(master=masterFrame)
        hScroll = ttk.Scrollbar(
            master=hScrollFrame, orient=tk.HORIZONTAL, command=canvas.xview
        )
        hScroll.pack(side=tk.BOTTOM, expand=False, fill=tk.X)
        hScrollFrame.pack(side=tk.TOP, expand=False, fill=tk.X)

        canvas.configure(yscrollcommand=vScroll.set, xscrollcommand=hScroll.set)
        canvas.bind(
            "<Configure>",
            lambda event: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        figFrame = FigureCanvasTkAgg(figure=fig, master=canvas)
        figFrame.draw()
        figCanvas = figFrame.get_tk_widget()

        canvas.create_window((0, 0), window=figCanvas, anchor="nw", tags="figCanvas")

        # Function to handle mousewheel scrolling with smoother increment
        def _on_mousewheel(event):
            increment = -1 * (
                event.delta / 120
            )  # Smaller increment for smoother scrolling
            canvas.yview_scroll(int(increment), "units")

        # Bind scrolling events to the canvas
        canvas.bind(
            "<Enter>", lambda event: canvas.bind_all("<MouseWheel>", _on_mousewheel)
        )
        canvas.bind(
            "<Enter>", lambda event: canvas.bind_all("<Button-4>", _on_mousewheel)
        )
        canvas.bind(
            "<Enter>", lambda event: canvas.bind_all("<Button-5>", _on_mousewheel)
        )
        canvas.bind("<Leave>", lambda event: canvas.unbind_all("<MouseWheel>"))

    def hide(self):
        self.grid_forget()


class Yer(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)

        self.lab = ttk.Label(master=self, text="hey")
        self.lab.grid(row=10, column=0)
