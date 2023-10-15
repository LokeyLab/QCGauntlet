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


# class DisplayFigure(ttk.Frame):
#     def __init__(self, fig: list, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.figs = fig if isinstance(fig, list) else [fig]
#         self.figHeight = np.sum(fig.bbox.ymax - fig.bbox.ymin for fig in self.figs)

#         self.canvas = self.__createFullCanvas()
#         self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

#         # Add vertical scrollbar
#         v_scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
#         v_scrollbar.place(relx=1, rely=0, relheight=1, anchor=NE)
#         self.canvas.config(yscrollcommand=v_scrollbar.set)

#         # Add horizontal scrollbar
#         h_scrollbar = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.canvas.xview)
#         h_scrollbar.place(relx=0, rely=1, relwidth=1, anchor="sw")

#         self.canvas.config(xscrollcommand=h_scrollbar.set)
#         self.canvas.config(scrollregion=(0, 0, 0, self.figHeight))

#         self.canvas.bind("<Configure>", self.__configure_canvas)

#         self.canvas.bind(
#             "<MouseWheel>",
#             lambda e: self.canvas.yview_scroll(-int(e.delta / 60), "units"),
#         )

#     def __createFullCanvas(self, sepHeight=10):
#         canvas = tk.Canvas(self)
#         # canvas.pack(side=LEFT, fill=BOTH, expand=True)

#         yOffset = 0
#         separator_height = sepHeight
#         for fig in self.figs:
#             fCanvas = FigureCanvasTkAgg(figure=fig, master=canvas)
#             fCanvas.draw()
#             canvas.create_window(
#                 0, yOffset, window=fCanvas.get_tk_widget(), anchor="nw"
#             )
#             yOffset += fig.bbox.ymax - fig.bbox.ymin

#             separator = ttk.Frame(
#                 canvas,
#                 height=separator_height,
#                 width=canvas.winfo_width(),
#                 relief=tk.SUNKEN,
#             )
#             canvas.create_window(0, yOffset, window=separator, anchor="nw")
#             yOffset += separator_height
#         return canvas

#     def __configure_canvas(self, event):
#         self.canvas.config(scrollregion=self.canvas.bbox("all"))


class DisplayFigure(ttk.Frame):
    def __init__(self, fig: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.figs = fig if isinstance(fig, list) else [fig]
        self.figHeight = np.sum(fig.bbox.ymax - fig.bbox.ymin for fig in self.figs)

        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add vertical scrollbar
        v_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scrollbar.place(relx=1, rely=0, relheight=1, anchor=tk.NE)
        self.canvas.config(yscrollcommand=v_scrollbar.set)

        # Add horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(
            self, orient=tk.HORIZONTAL, command=self.canvas.xview
        )
        h_scrollbar.place(relx=0, rely=1, relwidth=1, anchor=tk.SW)
        self.canvas.config(xscrollcommand=h_scrollbar.set)
        self.canvas.config(scrollregion=(0, 0, 0, self.figHeight))

        # Zoom in and zoom out buttons
        self.zoom_in_button = ttk.Button(
            self, text="Zoom In", command=self.__zoom_in, width=10
        )
        self.zoom_in_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.zoom_out_button = ttk.Button(
            self, text="Zoom Out", command=self.__zoom_out, width=10
        )
        self.zoom_out_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.__create_full_canvas()

        self.canvas.bind("<Configure>", self.__configure_canvas)

        self.canvas.bind(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(-int(e.delta / 60), "units"),
        )

    def __create_full_canvas(self, sep_height=10):
        yOffset = 0
        separator_height = sep_height
        for fig in self.figs:
            fCanvas = FigureCanvasTkAgg(figure=fig, master=self.canvas)
            fCanvas.draw()
            canvas_window = self.canvas.create_window(
                0, yOffset, window=fCanvas.get_tk_widget(), anchor=tk.NW
            )
            yOffset += fig.bbox.ymax - fig.bbox.ymin

            separator = ttk.Frame(
                self.canvas,
                height=separator_height,
                width=self.canvas.winfo_width(),
                relief=tk.SUNKEN,
            )
            self.canvas.create_window(0, yOffset, window=separator, anchor=tk.NW)
            yOffset += separator_height

    def __configure_canvas(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def __zoom(self, factor):
        # Get the current scale factor of the canvas
        current_scale = self.canvas.scale(tk.ALL, 0, 0)

        # Calculate the new scale factor after zooming
        new_scale = current_scale * (1.1**factor)

        # Get the current scroll position of the canvas
        x_scroll_pos = self.canvas.xview()[0]
        y_scroll_pos = self.canvas.yview()[0]

        # Apply the new scale factor to each canvas item individually
        for item in self.canvas.find_all():
            x, y, width, height = self.canvas.bbox(item)
            center_x, center_y = (x + width) / 2, (y + height) / 2

            # Scale the item around its center
            self.canvas.scale(item, center_x, center_y, new_scale, new_scale)

        # Adjust the scroll position to maintain the view
        self.canvas.xview_moveto(x_scroll_pos)
        self.canvas.yview_moveto(y_scroll_pos)

        # Update the scroll region after zooming
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

        # Note: You might need to adjust the zoom factor (1.1) for your specific use case

    def __zoom_in(self):
        self.__zoom(1)

    def __zoom_out(self):
        self.__zoom(-1)


# Usage example:
# figs = [...]  # List of matplotlib figures
# root = tk.Tk()
# display = DisplayFigure(figs, root)
# display.pack(fill=tk.BOTH, expand=True)
# root.mainloop()
