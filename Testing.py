import unittest
import tkinter as tk
from MyVideoCapture import MyVideoCapture
from FilterFrame import FilterFrame
from ImageViewer import ImageViewer
import numpy as np
import cv2


class MyTestCase(unittest.TestCase):
    def test_capture_type(self):
        cap = MyVideoCapture()
        self.assertEqual(type(cap.get_frame()[1]), np.ndarray)

    def test_capture_shape(self):
        cap = MyVideoCapture()
        self.assertEqual(cap.get_frame()[1].shape, (480, 640, 3))

    def test_filterFrame_sepia(self):
        img = cv2.imread("Testing.jpg")
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        img = cv2.filter2D(img, -1, kernel)
        filter1 = FilterFrame(master=testFrame())
        filter1._FilterFrame__sepia()
        self.assertTrue(img.all() == filter1.filtered_image.all())

    def test_filterFrame_emboss(self):
        img = cv2.imread("Testing.jpg")
        kernel = np.array([[0, -1, -1],
                           [1, 0, -1],
                           [1, 1, 0]])
        img = cv2.filter2D(img, -1, kernel)
        filter1 = FilterFrame(master=testFrame())
        filter1._FilterFrame__emboss()
        self.assertTrue(img.all() == filter1.filtered_image.all())

    def test_filterFrame_gaussian_blur(self):
        img = cv2.imread("Testing.jpg")
        img = cv2.GaussianBlur(img, (41, 41), 0)
        filter1 = FilterFrame(master=testFrame())
        filter1._FilterFrame__gaussian_blur()
        self.assertTrue(img.all() == filter1.filtered_image.all())

    def test_filterFrame_median_blur(self):
        img = cv2.imread("Testing.jpg")
        img = cv2.GaussianBlur(img, (41, 41), 0)
        filter1 = FilterFrame(master=testFrame())
        filter1._FilterFrame__median_blur()
        self.assertTrue(img.all() == filter1.filtered_image.all())

    def test_filterFrame_negative(self):
        img = cv2.imread("Testing.jpg")
        img = cv2.bitwise_not(img)
        filter1 = FilterFrame(master=testFrame())
        filter1._FilterFrame__negative()
        self.assertTrue(img.all() == filter1.filtered_image.all())

    def test_filterFrame_black_white(self):
        img = cv2.imread("Testing.jpg")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.cv2.COLOR_GRAY2BGR)
        filter1 = FilterFrame(master=testFrame())
        filter1._FilterFrame__black_white()
        self.assertTrue(img.all() == filter1.filtered_image.all())


class testFrame(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        self.filename = ""
        self.original_image = cv2.imread("Testing.jpg")
        self.processed_image = cv2.imread("Testing.jpg")
        self.is_image_selected = False
        self.is_draw_state = False
        self.is_crop_state = False

        self.filter_frame = None
        self.adjust_frame = None


if __name__ == '__main__':
    unittest.main()
