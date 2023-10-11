import tkinter as tk
from tkinter import ttk, filedialog
from ttkbootstrap import Style


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
