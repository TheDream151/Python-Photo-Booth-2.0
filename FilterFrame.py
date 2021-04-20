from tkinter import Toplevel, Button, RIGHT
import numpy as np
import cv2


class FilterFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.original_image = self.master.processed_image
        self.filtered_image = None

        self.negative_button = Button(master=self, text="Negative")
        self.black_white_button = Button(master=self, text="Black White")
        self.sepia_button = Button(master=self, text="Sepia")
        self.emboss_button = Button(master=self, text="Emboss")
        self.gaussian_blur_button = Button(master=self, text="Gaussian Blur")
        self.median_blur_button = Button(master=self, text="Median Blur")
        self.cancel_button = Button(master=self, text="Cancel")
        self.apply_button = Button(master=self, text="Apply")

        self.negative_button.bind("<ButtonRelease>", self.__negative_button_released)
        self.black_white_button.bind("<ButtonRelease>", self.__black_white_released)
        self.sepia_button.bind("<ButtonRelease>", self.__sepia_button_released)
        self.emboss_button.bind("<ButtonRelease>", self.__emboss_button_released)
        self.gaussian_blur_button.bind("<ButtonRelease>", self.__gaussian_blur_button_released)
        self.median_blur_button.bind("<ButtonRelease>", self.__median_blur_button_released)
        self.apply_button.bind("<ButtonRelease>", self.__apply_button_released)
        self.cancel_button.bind("<ButtonRelease>", self.__cancel_button_released)

        self.negative_button.pack()
        self.black_white_button.pack()
        self.sepia_button.pack()
        self.emboss_button.pack()
        self.gaussian_blur_button.pack()
        self.median_blur_button.pack()
        self.cancel_button.pack(side=RIGHT)
        self.apply_button.pack()

    def __negative_button_released(self, event):
        self.__negative()
        self.__show_image()

    def __black_white_released(self, event):
        self.__black_white()
        self.__show_image()

    def __sepia_button_released(self, event):
        self.__sepia()
        self.__show_image()

    def __emboss_button_released(self, event):
        self.__emboss()
        self.__show_image()

    def __gaussian_blur_button_released(self, event):
        self.__gaussian_blur()
        self.__show_image()

    def __median_blur_button_released(self, event):
        self.__gaussian_blur()
        self.__show_image()

    def __apply_button_released(self, event):
        self.master.processed_image = self.filtered_image
        self.__show_image()
        self.__close()

    def __cancel_button_released(self, event):
        self.master.image_viewer.show_image()
        self.__close()

    def __show_image(self):
        self.master.image_viewer.show_image(img=self.filtered_image)

    def __negative(self):
        self.filtered_image = cv2.bitwise_not(self.original_image)

    def __black_white(self):
        self.filtered_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        self.filtered_image = cv2.cvtColor(self.filtered_image, cv2.COLOR_GRAY2BGR)

    def __sepia(self):
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])

        self.filtered_image = cv2.filter2D(self.original_image, -1, kernel)

    def __emboss(self):
        kernel = np.array([[0, -1, -1],
                           [1, 0, -1],
                           [1, 1, 0]])

        self.filtered_image = cv2.filter2D(self.original_image, -1, kernel)

    def __gaussian_blur(self):
        self.filtered_image = cv2.GaussianBlur(self.original_image, (41, 41), 0)

    def __median_blur(self):
        self.filtered_image = cv2.medianBlur(self.original_image, 41)

    def __close(self):
        self.destroy()
