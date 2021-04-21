import unittest
from MyVideoCapture import MyVideoCapture
from FilterFrame import FilterFrame
import numpy as np
import cv2


class MyTestCase(unittest.TestCase):
    def test_capture(self):
        cap = MyVideoCapture()
        self.assertEqual(type(cap.get_frame()[1]), np.ndarray)

    def test_filterFrame(self):
        img = cv2.imread("Testing.jpg")

        filter = FilterFrame()
        filter.original_image = img
        filter._FilterFrame__sepia(filter)
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        img_test = cv2.filter2D(img, -1, kernel)
        img = filter.filtered_image
        self.assertEqual(img, img_test)


if __name__ == '__main__':
    unittest.main()
