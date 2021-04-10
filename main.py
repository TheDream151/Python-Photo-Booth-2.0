# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import cv2
import PIL
import tkinter as tk
from editorScreen import editorScreen
from imageDisplay import imageDisplay

class Main(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.filename = ""
        self.originImage = None
        self.editedImage = None
        self.imageSelected = None
        self.isCrop = None

        self.filterFrame = None
        self.adjustSize = None

        self.title("PhotoBooth Program")

        self.editorScreen = editorScreen(master = self)
        splitter = tk.SEPARATOR(master= self, orient=tk.HORIZONTAL)
        self.imageDisplay = imageDisplay(master=self)

        self.editMenu.pack(pady = 10)
        splitter.pack(fill=tk.X, padx = 20, pady = 5)
        self.imageViewer.pack(fill=tk.BOTH, padx=20, pady=10, expand=1)


        self.editorScreen.pack(pady=10)
        splitter.imageDisplay.pack(fill=tk.X, padx=20, pady=10, expand=1)


