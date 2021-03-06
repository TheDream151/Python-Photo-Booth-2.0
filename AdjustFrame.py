from tkinter import Toplevel, Label, Scale, Button, HORIZONTAL, RIGHT
import cv2


class AdjustFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.brightness_value = 0
        self.previous_brightness_value = 0

        self.original_image = self.master.processed_image
        self.processing_image = self.master.processed_image

        self.brightness_label = Label(self, text="Brightness")
        self.brightness_scale = Scale(self, from_=0, to_=2, length=250, resolution=0.1,
                                      orient=HORIZONTAL)
        self.r_label = Label(self, text="R")
        self.r_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,
                             orient=HORIZONTAL)
        self.g_label = Label(self, text="G")
        self.g_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,
                             orient=HORIZONTAL)
        self.b_label = Label(self, text="B")
        self.b_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,
                             orient=HORIZONTAL)
        self.apply_button = Button(self, text="Apply")
        self.preview_button = Button(self, text="Preview")
        self.cancel_button = Button(self, text="Cancel")

        self.brightness_scale.set(1)

        self.apply_button.bind("<ButtonRelease>", self.__apply_button_released)
        self.preview_button.bind("<ButtonRelease>", self.__show_button_release)
        self.cancel_button.bind("<ButtonRelease>", self.__cancel_button_released)

        self.brightness_label.pack()
        self.brightness_scale.pack()
        self.r_label.pack()
        self.r_scale.pack()
        self.g_label.pack()
        self.g_scale.pack()
        self.b_label.pack()
        self.b_scale.pack()
        self.cancel_button.pack(side=RIGHT)
        self.preview_button.pack(side=RIGHT)
        self.apply_button.pack()

    def __apply_button_released(self, event):
        """
        Applies the change in attributes to the image on button release
        @:param event this parameter takes the button's event, this is not used but is required for the button to call
        the function
        """
        self.__show_button_release(event)
        self.master.processed_image = self.processing_image
        self.close()

    def __show_button_release(self, event):
        """
        Shows a preview of the image with the change in attributes on button release
        @:param event this parameter takes the button's event, this is not used but is required for the button to call
        the function
        """
        self.processing_image = cv2.convertScaleAbs(self.original_image, alpha=self.brightness_scale.get())
        b, g, r = cv2.split(self.processing_image)

        for b_value in b:
            cv2.add(b_value, self.b_scale.get(), b_value)
        for g_value in g:
            cv2.add(g_value, self.g_scale.get(), g_value)
        for r_value in r:
            cv2.add(r_value, self.r_scale.get(), r_value)

        self.processing_image = cv2.merge((b, g, r))
        self.__show_image(self.processing_image)

    def __cancel_button_released(self, event):
        """
        Closes the window
        @:param event this parameter takes the button's event, this is not used but is required for the button to call
        the function
        """
        self.close()

    def __show_image(self, img=None):
        """
        Displays the image in the image viewer class
        """
        self.master.image_viewer.show_image(img=img)

    def close(self):
        """
        Displays the image and closes the frame
        """
        self.__show_image()
        self.destroy()
