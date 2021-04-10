from tkinter import filedialog
from tkinter import *
import cv2


class editorScreen(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master)

        self.newEdit = Button(self, text="New Image Edit")
        self.newPicture = Button(self, text="Take New Picture")
        self.saveButton = Button(self, text="Save As")
        self.cropButton = Button(self, text="Crop Image")
        self.filterButton = Button(self, text="Filters")
        self.adjustableFilter = Button(self, text="Adjustable Filters")
        self.clearButton = Button(self, text="Clear Picture")


        self.newEdit.bind("<ButtonRelease", self.newEdit_click)
        self.newPicture.bind("<ButtonRelease", self.newPicture_click)
        self.saveButton.bind("<ButtonRelease", self.saveButton_click)
        self.cropButton.bind("<ButtonRelease", self.cropButton_click)
        self.filterButton.bind("<ButtonRelease", self.filterButton_click)
        self.adjustableFilter.bind("<ButtonRelease", self.adjustableFilter_click)
        self.clearButton.bind("<ButtonRelease", self.clearButton_click)

        self.newEdit.pack(side=CENTER)
        self.newPicture.pack(side=CENTER)
        self.saveButton.pack(side=CENTER)
        self.cropButton.pack(side=CENTER)
        self.filterButton.pack(side=CENTER)
        self.adjustableFilter.pack(side=CENTER)
        self.clearButton.pack(side=CENTER)


    def newEdit_click(self, event):
            filename = filedialog.askopenfilename()
            image = cv2.imread(filename)

            if image is not None:
                self.master.filename = filename
                self.master.originImage = image.copy()



    def newPicture_click(self, event):
        print("hi")

    def newPicture_click(self, event):
        print("Hi")


    def saveButton_click(self, event):
        print("Hi")

    def cropButton_click(self, event):
        print("Hi")

    def filterButton_click(self, event):
        print("Hi")

    def adjustableFilter_click(self, event):
        print("Hi")

    def clearButton_click(self, event):
        print("Hi")