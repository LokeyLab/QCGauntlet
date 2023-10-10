import tkinter as tk
from tkinter import ttk, filedialog
from ttkbootstrap import Style


class PlaceholderEntry(ttk.Entry):
    def __init__(self, master=None, placeholder="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.insert(tk.END, self.placeholder)
        self.bind("<FocusIn>", self.on_entry_click)
        self.bind("<FocusOut>", self.on_focus_out)
        self.configure(foreground="#888888")  # Set initial text color to gray

    def on_entry_click(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.configure(foreground="#FFFFFF")  # Change text color to black

    def on_focus_out(self, event):
        if not self.get():
            self.insert(tk.END, self.placeholder)
            self.configure(foreground="#888888")
