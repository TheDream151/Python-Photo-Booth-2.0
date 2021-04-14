import time
import tkinter
import tkinter as tk
from tkinter import ttk

import PIL
import cv2
from PIL import ImageTk

from MyVideoCaputure import MyVideoCapture


class Camera(tk.Frame):
    def __init__(self, parent, controller, video_source=0):
        self.video_source = 0
        tk.Frame.__init__(self, parent)
        self.vid = MyVideoCapture()
        self.controller = controller
        self.parent = parent
        # label of frame Layout 2

        self.canvas = tkinter.Canvas(self, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        self.btn_snapshot = ttk.Button(self, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        self.delay = 15
        self.update()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg",
                        cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.parent.after(self.delay, self.update)