import tkinter as tk
from tkinter import ttk


class Camera(tk.Frame):
    def __init__(self, parent, controller, video_source=0):
        self.video_source = 0
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text="Startpage")

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=4, padx=10, pady=10)
