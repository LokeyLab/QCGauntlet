import pandas as pd
import numpy as np

import tkinter as tk
from tkinter import ttk, filedialog
from ttkbootstrap import Style
from gui_utils.ttkUtils import *

# import ttkbootstrap as ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        style = Style(theme="darkly")
        self.title("QCGauntlet.py")
        self.geometry("1280x720")

        frame = ttk.Frame(self, borderwidth=2, relief="solid")

        frame.grid(row=0, column=0, columnspan=2, pady=10, padx=10)
        frame.pack(side=tk.TOP, anchor="w", padx=10, pady=10)

        title_label = tk.Label(
            frame, text="Main File Input and Options", font=("Arial", 14, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2)

        # Create the first file browser
        self.file_path_var1 = tk.StringVar()
        self.textbox1 = PlaceholderEntry(
            frame,
            textvariable=self.file_path_var1,
            width=10,
            placeholder="Main Condition File (.csv)",
        )
        self.textbox1.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.file_browser1 = ttk.Button(
            frame,
            text="Browse File...",
            command=self.cond1,
            width=10,
        )
        self.file_browser1.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        # Create the second file browser
        self.file_path_var2 = tk.StringVar()
        self.textbox2 = PlaceholderEntry(
            frame,
            textvariable=self.file_path_var2,
            width=10,
            placeholder="Alt. Condition (.csv)",
        )
        self.textbox2.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.file_browser2 = ttk.Button(
            frame,
            text="Browse File...",
            command=self.cond2,
            width=10,
        )
        self.file_browser2.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        self.file_path_var3 = tk.StringVar()
        self.textbox3 = PlaceholderEntry(
            frame,
            textvariable=self.file_path_var3,
            width=10,
            placeholder="Key file (.csv)",
        )
        self.textbox3.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.file_browser3 = ttk.Button(
            frame, text="Browse File...", command=self.key, width=10
        )
        self.file_browser3.grid(row=3, column=1, padx=10, pady=10, sticky="e")

        # Add title for the pair of textboxes
        pair_title_label = tk.Label(
            frame, text="Index Rename Properties", font=("Arial", 12, "bold")
        )
        pair_title_label.grid(row=4, column=0, columnspan=2, pady=(10, 0))

        # Create textboxes for General Plate Names and Proper Names
        self.general_plate_var = tk.StringVar()
        # self.general_plate_entry = ttk.Entry(
        #     frame, textvariable=self.general_plate_var, width=20
        # )
        # self.general_plate_entry.insert(0, "General Plate Names")
        self.general_plate_entry = PlaceholderEntry(
            frame,
            textvariable=self.general_plate_var,
            width=20,
            placeholder="Enter General Plate Names",
        )
        self.general_plate_entry.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        self.proper_names_var = tk.StringVar()
        self.proper_names_entry = PlaceholderEntry(
            frame,
            textvariable=self.proper_names_var,
            width=20,
            placeholder="Enter Proper Plate Names",
        )
        self.proper_names_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        frame.columnconfigure(0, weight=2)  # Give more weight to column 0
        frame.columnconfigure(1, weight=0)

    def cond1(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_var1.set(file_path)

    def cond2(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_var2.set(file_path)

    def key(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_var3.set(file_path)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
