import tkinter as tk
from tkinter import ttk


class Image_Editor(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 1")
        label.grid(row=0, column=4, padx=10, pady=10)

