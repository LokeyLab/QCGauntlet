import tkinter as tk
from tkinter import ttk, filedialog
from ttkbootstrap import Style
import os
from gui_utils import *


class FileBrowsing(tk.Frame):
    def __init__(self, parent, cursors, bootstyle, **kwargs):
        super().__init__(parent, **kwargs)
        self.cursors = cursors
        self.bootstyle = bootstyle

        self.file_path_var1 = tk.StringVar()
        self.textbox1 = PlaceholderEntry(
            parent,
            textvariable=self.file_path_var1,
            width=10,
            placeholder="Main Condition File (.csv)",
        )
        self.textbox1.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.file_browser1 = ttk.Button(
            parent,
            text="Browse File...",
            command=self.cond1,
            width=10,
            cursor=self.cursors,
            bootstyle=self.bootstyle,
        )
        self.file_browser1.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        # Create the second file browser
        self.file_path_var2 = tk.StringVar()
        self.textbox2 = PlaceholderEntry(
            parent,
            textvariable=self.file_path_var2,
            width=10,
            placeholder="Alt. Condition (.csv)",
        )
        self.textbox2.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.file_browser2 = ttk.Button(
            parent,
            text="Browse File...",
            command=self.cond2,
            width=10,
            cursor=self.cursors,
            bootstyle=self.bootstyle,
        )
        self.file_browser2.grid(row=3, column=1, padx=10, pady=10, sticky="e")

        self.file_path_var3 = tk.StringVar()
        self.textbox3 = PlaceholderEntry(
            parent,
            textvariable=self.file_path_var3,
            width=10,
            placeholder="Key file (.csv)",
        )
        self.textbox3.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        self.file_browser3 = ttk.Button(
            parent,
            text="Browse File...",
            command=self.key,
            width=10,
            cursor=self.cursors,
            bootstyle=self.bootstyle,
        )
        self.file_browser3.grid(row=4, column=1, padx=10, pady=10, sticky="e")

    def cond1(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_var1.set(file_path)
            if os.path.isfile(self.textbox1.get()):
                return self.textbox2.get()
            return None

    def cond2(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_var2.set(file_path)

            if os.path.isfile(self.textbox2.get()):
                return self.textbox2.get()
            return None

    def key(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_var3.set(file_path)

            if os.path.isfile(self.textbox3.get()):
                return self.textbox3.get()
            return None

    def getFiles(self):
        cond1 = None
        if os.path.isfile(self.textbox1.get()):
            cond1 = self.textbox1.get()

        cond2 = None
        if os.path.isfile(self.textbox2.get()):
            cond2 = self.textbox2.get()

        key = None
        if os.path.isfile(self.textbox3.get()):
            key = self.textbox3.get()

        return cond1, cond2, key


class programOptions(tk.Frame):
    def __init__(self, parent, cursors, bootstyle, **kwargs):
        super().__init__(parent, **kwargs)
        self.threshold = 0.5

        # Create textboxes for General Plate Names and Proper Names
        pair_title_label = tk.Label(
            parent, text="Index Rename Properties", font=("Arial", 12, "bold")
        )
        pair_title_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        self.general_plate_var = tk.StringVar()
        self.general_plate_entry = PlaceholderEntry(
            parent,
            textvariable=self.general_plate_var,
            width=20,
            placeholder="Enter General Plate Names",
        )
        self.general_plate_entry.grid(row=6, column=0, padx=5, pady=5, sticky="w")

        self.proper_names_var = tk.StringVar()
        self.proper_names_entry = PlaceholderEntry(
            parent,
            textvariable=self.proper_names_var,
            width=20,
            placeholder="Enter Proper Plate Names",
        )
        self.proper_names_entry.grid(row=6, column=1, padx=5, pady=5, sticky="e")

        # self.submit_button = ttk.Button(
        #     parent, text="Submit", command=self.submit_action, cursor=self.cursors
        # )
        # self.submit_button.grid(row=6, column=0, columnspan=2, pady=10)
        pair_title_label2 = tk.Label(
            parent, text="General options", font=("Arial", 12, "bold")
        )
        pair_title_label2.grid(row=7, column=0, columnspan=2, pady=(10, 0))
        seperator = ttk.Separator(master=parent, orient="horizontal")
        seperator.grid(row=8, column=0, columnspan=2, sticky="ew", pady=5, padx=10)

        self.thresholdEntry = ttk.Entry(
            master=parent,
            textvariable=self.threshold,
            width=20,
        )
        self.thresholdEntry.grid(row=9, column=0, padx=10, pady=5, sticky="w")
        self.thresholdTitle = ttk.Label(
            master=parent, text="Threshold value (default: 0.5)", font=("arial", 12)
        )
        self.thresholdEntry.insert(0, "0.5")
        self.thresholdTitle.grid(row=9, column=1, padx=10, pady=5, sticky="w")

        self.indexColEntry = ttk.Entry(master=parent, width=20)
        self.indexColEntry.grid(row=10, column=0, padx=10, pady=5, sticky="w")
        self.indexColEntry.insert(0, "0")
        self.indexColTitle = ttk.Label(
            master=parent, text="Index Column (default: 0)", font=("arial", 12)
        )
        self.indexColTitle.grid(row=10, column=1, padx=10, pady=5, sticky="w")

        self.controlTitleHeading = ttk.Label(
            master=parent, text="Control Title Labeling", font=("Arial", 12)
        )
        self.controlTitleHeading.grid(row=11, column=0, columnspan=2, padx=10, pady=5)

        self.controlTitle1Entry = PlaceholderEntry(
            master=parent, placeholder="Control Title 1", width=20
        )
        self.controlTitle1Entry.grid(row=12, column=0, padx=10, pady=5, sticky="w")
        self.controlTitle2Entry = PlaceholderEntry(
            master=parent, placeholder="Control Title 2", width=20
        )
        self.controlTitle2Entry.grid(row=12, column=1, padx=10, pady=5, sticky="e")

        self.fileRenameTitle = ttk.Label(
            master=parent, text="File Renaming Options", font=("arial", 12)
        )
        self.fileRenameTitle.grid(row=13, column=0, columnspan=2, padx=10, pady=5)
        self.fileRenameEntry1 = PlaceholderEntry(
            master=parent, placeholder="Main condition rename", width=20
        )
        self.fileRenameEntry2 = PlaceholderEntry(
            master=parent, placeholder="Alt condition rename", width=20
        )
        self.fileRenameEntry1.grid(row=14, column=0, padx=10, pady=5, sticky="w")
        self.fileRenameEntry2.grid(row=14, column=1, padx=10, pady=5, sticky="e")

    def getThreshold(self):
        return float(self.thresholdEntry.get())

    def getIndexCol(self):
        return int(self.indexColEntry.get())

    def getControlTitles(self):
        titles = [self.controlTitle1Entry.get()]
        if (
            self.controlTitle2Entry.get()
            != self.controlTitle2Entry.getPlaceholderText()
        ):
            titles = [self.controlTitle1Entry.get(), self.controlTitle2Entry.get()]
        return titles

    def getFileRenames(self):
        renames = [self.fileRenameEntry1.get()]
        if self.fileRenameEntry2.get() != self.fileRenameEntry2.getPlaceholderText():
            renames = [self.fileRenameEntry1.get(), self.fileRenameEntry2.get()]
        return renames

    def getIndexRename(self):
        genPlate = None
        if (
            self.general_plate_entry.get()
            != self.general_plate_entry.getPlaceholderText()
        ):
            genPlate = self.general_plate_entry.get()

        properName = None
        if (
            self.proper_names_entry.get()
            != self.proper_names_entry.getPlaceholderText()
        ):
            properName = self.proper_names_entry.get()
        return [genPlate, properName]
