import time
import tkinter
import tkinter as tk
from tkinter import ttk

import PIL
import cv2
from PIL import ImageTk

from MyVideoCapture import MyVideoCapture


class Camera(tk.Frame):
    def __init__(self, parent, controller, video_source=0):
        self.video_source = video_source
        tk.Frame.__init__(self, parent)
        self.vid = MyVideoCapture()
        self.controller = controller
        self.parent = parent
        self.prev = time.time()
        self.timer = 10
        self.countdown = False
        # label of frame Layout 2

        self.canvas = tkinter.Canvas(self, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        self.btn_snapshot = ttk.Button(self, text="Snapshot", width=25, command=self.snapshot)
        self.filter = ttk.Button(self, text="Toggle Filter", width=25, command=self.vid.toggle_filter)
        self.btn_timed_snapshot = ttk.Button(self, text="Timed Snapshot", width=25, command=self.toggle_time)
        self.btn_snapshot.pack(side=tkinter.LEFT, expand=True)
        self.filter.pack(side=tkinter.LEFT, expand=True)
        self.btn_timed_snapshot.pack(side=tkinter.LEFT, expand=True)

        self.delay = 15
        self.update()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            cv2.imwrite("photos/frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg",
                        cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def toggle_time(self):
        self.prev = time.time()
        if self.countdown:
            self.timer = 10
            self.countdown = False
        else:
            self.countdown = True

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if self.countdown:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, str(self.timer),
                        (200, 250), font,
                        7, (0, 255, 255),
                        4, cv2.LINE_AA)

            # current time
            cur = time.time()
            if cur - self.prev >= 1:
                self.prev = cur
                self.timer = self.timer - 1

            if self.timer == 0:
                self.snapshot()
                self.timer = 10
                self.countdown = False

        if ret:
            self.photo = ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.parent.after(self.delay, self.update)
