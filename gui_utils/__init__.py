import tkinter as tk
from tkinter import filedialog, constants
from ttkbootstrap import Style, ttk
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.constants import *

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backends.backend_pdf import PdfPages


class PlaceholderEntry(ttk.Entry):
    def __init__(self, master=None, placeholder="", **kwargs):
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.default_fg_color = self["foreground"]

        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        self.set_placeholder()

    def on_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self.config(foreground=self.default_fg_color)

    def on_focus_out(self, event):
        self.set_placeholder()

    def set_placeholder(self):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(foreground="gray")

    def getPlaceholderText(self):
        return self.placeholder


class DisplayFigure(ttk.Frame):
    def __init__(self, fig: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.figs = fig
        self.figHeight = np.sum(fig.bbox.ymax - fig.bbox.ymin for fig in self.figs)

        self.canvas = self.__createFullCanvas()
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Add vertical scrollbar
        v_scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        v_scrollbar.place(relx=1, rely=0, relheight=1, anchor=NE)
        self.canvas.config(yscrollcommand=v_scrollbar.set)

        # Add horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.canvas.xview)
        h_scrollbar.place(relx=0, rely=1, relwidth=1, anchor="sw")

        self.canvas.config(xscrollcommand=h_scrollbar.set)
        self.canvas.config(scrollregion=(0, 0, 0, self.figHeight))

        self.canvas.bind("<Configure>", self.__configure_canvas)

        self.canvas.bind(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(-int(e.delta / 60), "units"),
        )

    def __createFullCanvas(self):
        canvas = tk.Canvas(self)
        # canvas.pack(side=LEFT, fill=BOTH, expand=True)

        yOffset = 0
        for fig in self.figs:
            fCanvas = FigureCanvasTkAgg(figure=fig, master=canvas)
            fCanvas.draw()
            canvas.create_window(
                0, yOffset, window=fCanvas.get_tk_widget(), anchor="nw"
            )
            yOffset += fig.bbox.ymax - fig.bbox.ymin
        return canvas

    def __configure_canvas(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
