from tkinter import Frame, Button, LEFT
from tkinter import filedialog
from FilterFrame import FilterFrame
from AdjustFrame import AdjustFrame
from tkinter import colorchooser

import cv2


class EditBar(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master)

        self.new_button = Button(self, text="Open")
        self.save_button = Button(self, text="Save")
        self.save_as_button = Button(self, text="Save As")
        self.draw_button = Button(self, text="Draw")
        self.crop_button = Button(self, text="Crop")
        self.filter_button = Button(self, text="Filter")
        self.adjust_button = Button(self, text="Adjust")
        self.clear_button = Button(self, text="Clear")
        self.color_button = Button(self, text="Select Color", command=self.__choose_color)

        self.new_button.bind("<ButtonRelease>", self.__new_button_released)
        self.save_button.bind("<ButtonRelease>", self.__save_button_released)
        self.save_as_button.bind("<ButtonRelease>", self.__save_as_button_released)
        self.draw_button.bind("<ButtonRelease>", self.__draw_button_released)
        self.crop_button.bind("<ButtonRelease>", self.__crop_button_released)
        self.filter_button.bind("<ButtonRelease>", self.__filter_button_released)
        self.adjust_button.bind("<ButtonRelease>", self.__adjust_button_released)
        self.clear_button.bind("<ButtonRelease>", self.__clear_button_released)

        self.new_button.pack(side=LEFT)
        self.save_button.pack(side=LEFT)
        self.save_as_button.pack(side=LEFT)
        self.draw_button.pack(side=LEFT)
        self.color_button.pack(side=LEFT)
        self.crop_button.pack(side=LEFT)
        self.filter_button.pack(side=LEFT)
        self.adjust_button.pack(side=LEFT)
        self.clear_button.pack()

    def __new_button_released(self, event):
        """
        Open the file manager frame and has the user select an image on button press
        @:param event the button press event passed by the pressing of the button
        """
        if self.winfo_containing(event.x_root, event.y_root) == self.new_button:
            if self.master.is_draw_state:
                self.master.image_viewer.deactivate_draw()
            if self.master.is_crop_state:
                self.master.image_viewer.deactivate_crop()

            filename = filedialog.askopenfilename()
            image = cv2.imread(filename)

            if image is not None:
                self.master.filename = filename
                self.master.original_image = image.copy()
                self.master.processed_image = image.copy()
                self.master.image_viewer.show_image()
                self.master.is_image_selected = True

    def __save_button_released(self, event):
        """
        Saves the image in place on button press
        @:param event the button press event passed by the pressing of the button
        """
        if self.winfo_containing(event.x_root, event.y_root) == self.save_button:
            if self.master.is_image_selected:
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()

                save_image = self.master.processed_image
                image_filename = self.master.filename
                cv2.imwrite(image_filename, save_image)

    def __save_as_button_released(self, event):
        """
        Opens the file manager dialog and allows the user to save the image as a new file on button press
        @:param event the button press event passed by the pressing of the button
        """
        if self.winfo_containing(event.x_root, event.y_root) == self.save_as_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()

                original_file_type = self.master.filename.split('.')[-1]
                filename = filedialog.asksaveasfilename()
                filename = filename + "." + original_file_type

                save_image = self.master.processed_image
                cv2.imwrite(filename, save_image)

                self.master.filename = filename

    def __draw_button_released(self, event):
        """
        Toggles the drawing functionality of the program on button press
        @:param event the button press event passed by the pressing of the button
        """
        if self.winfo_containing(event.x_root, event.y_root) == self.draw_button:
            if self.master.is_image_selected:
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                else:
                    self.master.image_viewer.activate_draw()

    def __crop_button_released(self, event):
        """
        Toggles the cropping functionality of the program on button press
        @:param event the button press event passed by the pressing of the button
        """
        if self.winfo_containing(event.x_root, event.y_root) == self.crop_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                else:
                    self.master.image_viewer.activate_crop()

    def __filter_button_released(self, event):
        """
        Opens the filter frame on button press
        @:param event the button press event passed by the pressing of the button
        """
        if self.winfo_containing(event.x_root, event.y_root) == self.filter_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()

                self.master.filter_frame = FilterFrame(master=self.master)
                self.master.filter_frame.grab_set()

    def __adjust_button_released(self, event):
        """
        Opens the adjust frame on button press
        @:param event the button press event passed by the pressing of the button
        """
        if self.winfo_containing(event.x_root, event.y_root) == self.adjust_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()

                self.master.adjust_frame = AdjustFrame(master=self.master)
                self.master.adjust_frame.grab_set()

    def __clear_button_released(self, event):
        """
        Clears the edits to the image on button press
        @:param event the button press event passed by the pressing of the button
        """
        if self.winfo_containing(event.x_root, event.y_root) == self.clear_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()

                self.master.processed_image = self.master.original_image.copy()
                self.master.image_viewer.show_image()

    def __choose_color(self):
        """
        On button press opens the color picker frame
        """
        # variable to store hexadecimal code of color
        self.master.image_viewer.set_color_code(colorchooser.askcolor(title="Choose color"))
