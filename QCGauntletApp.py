import pandas as pd
import numpy as np
import sys

import tkinter as tk
from tkinter import filedialog
from ttkbootstrap import Style, ttk
from ttkbootstrap.constants import *
from gui_utils.ttkMainMenu import *
from gui_utils.ttkMainViews import *

import ttkbootstrap as ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        style = Style(theme="sandstone")
        self.title("QCGauntlet.py")
        self.geometry("1280x720")
        self.cursors = "dot"
        self.bootstyle = SUCCESS
        # title.pack(side=tk.TOP, anchor="nw", fill=tk.X)

        frame = ttk.Frame(self, borderwidth=2, relief="solid")

        title = ttk.Label(frame, text="QCGauntlet.py", font=("arial", 20, "bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(5, 30))
        frame.pack(side=tk.LEFT, anchor="sw", fill=tk.Y)

        title_label = tk.Label(
            frame, text="Main File Input and Options", font=("Arial", 14, "bold")
        )
        title_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        ######################### FILE BROWSING #########################
        self.fb = FileBrowsing(
            parent=frame, cursors=self.cursors, bootstyle=self.bootstyle
        )

        ######################### OPTIONS #########################
        self.optionsFrontEnd = programOptions(
            parent=frame, cursors=self.cursors, bootstyle=self.bootstyle
        )

        ######################### SUBMIT BUTTON #########################
        sep = ttk.Separator(master=frame, orient="horizontal")
        sep.grid(row=15, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

        self.submit = ttk.Button(
            master=frame,
            text="Analyze",
            command=self.submit_action,
            bootstyle=self.bootstyle,
            cursor=self.cursors,
            width=20,
        )
        self.submit.grid(row=16, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

        frame.columnconfigure(0, weight=100)  # Give more weight to column 0
        frame.columnconfigure(1, weight=0)

        ######################### MAIN VIEW #########################
        nbFrame = ttk.Frame(self)
        nbFrame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.nb = ttk.Notebook(master=nbFrame)

        self.cpScoreTab = CPActivityScores(self.nb, cursor=self.cursors)

        yer = Yer(self.nb)

        self.nb.add(self.cpScoreTab, text="cpscore")
        self.nb.add(yer, text="yeg")
        self.nb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.cpScoreTab.forget()
        self.nb.pack_forget()
        # nb.grid(row=0, column=3, padx=5, pady=10, sticky="ew")
        # nb.pack(expand=True, fill=tk.BOTH)

    def submit_action(self):
        # Get the input values from the textboxes
        cond1, cond2, key = self.fb.getFiles()
        renameColumns = self.optionsFrontEnd.getIndexRename()
        threshold = float(self.optionsFrontEnd.getThreshold())
        indexCol = int(self.optionsFrontEnd.getIndexCol())
        cntrlTitles = self.optionsFrontEnd.getControlTitles()
        actTitles = self.optionsFrontEnd.getFileRenames()

        main_condition_file = pd.read_csv(cond1, sep=",", index_col=indexCol)

        alt_condition_file = None
        if cond2 is not None:
            alt_condition_file = pd.read_csv(cond2, sep=",", index_col=indexCol)

        key_file = None
        if key is not None:
            key_file = pd.read_csv(key, sep=",")
            key_file.set_index(renameColumns[0], inplace=True)

        # Perform actions with the input values
        # (e.g., process files, perform computations, etc.)
        # loadcpscoreactivity data
        self.cpScoreTab.loadData(
            cond1=main_condition_file,
            cond2=alt_condition_file,
            map=key_file,
            activityTitles=actTitles,
            controlTitle=cntrlTitles,
            renameColumn=renameColumns[1],
        )

        # For demonstration, just print the input values
        self.nb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # print("Main Condition File:", main_condition_file)
        # print("Alt Condition File:", alt_condition_file)
        # print("Key File:", key_file)
        # print("General Plate Names:", renameColumns[0])
        # print("Proper Plate Names:", renameColumns[1])


def main():
    app = App()
    # app.resizable(False, False)
    app.mainloop()


if __name__ == "__main__":
    main()
