import tkinter as tk
from Camera_Frame import Camera
from Image_Editor import ImageEditor


class TkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create the file menu bar
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Camera", command=lambda: self.show_frame(Camera))
        file_menu.add_command(label="Image Editor", command=lambda: self.show_frame(ImageEditor))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menu_bar)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Camera, ImageEditor):
            frame = F(container, self)

            # initializing frames for Camera and Image Editor
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Camera)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
