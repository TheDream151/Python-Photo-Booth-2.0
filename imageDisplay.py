from tkinter import *
import cv2
from PIL import ImageTk


class imageDisplay(Frame):

    def __init__(self, master=None):
        Frame.__init__(self,master=master, bg="gray", width = 800, height = 800)

        self.displayedImage = None
        self.x = 0
        self.y = 0
        self.startCropX = 0
        self.startCropY = 0
        self.endCropX = 0
        self.endCropY = 0
        self.drawId = list()
        self.rectangleId = 0
        self.ratio = 0

        self.canvas = Canvas(self, bg  = "gray", width = 800, height = 800)
        self.canvas.place(relx=0.5, rely = 0.5, anchor =CENTER)

    def showImage(self, img=None):
        self.clear_canvas()

        if img is None:
            image = self.master.processed_image.copy()
        else:
            image = img

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = image.shape
        ratio = height / width


        self.displayedImage = cv2.resize(image, (width, height))
        self.displayedImage = ImageTk.PhotoImage(Image.fromarray(self.displayedImage))