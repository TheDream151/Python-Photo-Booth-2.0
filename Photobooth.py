import tkinter as tk
from Camera_Frame import Camera
# from test import Image_Editor
from Image_Editor import ImageEditor
import os

folder = r"/photos/"
cwd = os.getcwd()
path = cwd+folder
if not os.path.exists(path):
    os.makedirs(path)


class PhotoBooth(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Camera, ImageEditor):
            frame = F(container, self)

            # initializing frame of that object from
            # startPage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.__show_frame(Camera)
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Camera", command=lambda: self.__show_frame(Camera))
        file_menu.add_command(label="Image Editor", command=lambda: self.__show_frame(ImageEditor))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        self.config(menu=menu_bar)

    # to display the current frame passed as
    # parameter
    def __show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
