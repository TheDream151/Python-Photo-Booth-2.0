import cv2
import numpy as np


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        self.countdown = False
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # get facial classifiers
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

        # read images
        self.witch = cv2.imread('witch.png')
        self.filter_bool = False
        # get shape of witch
        self.original_witch_h, self.original_witch_w, self.witch_channels = self.witch.shape
        # convert to gray
        witch_gray = cv2.cvtColor(self.witch, cv2.COLOR_BGR2GRAY)
        # create mask and inverse mask of witch
        ret, self.original_mask = cv2.threshold(witch_gray, 10, 255, cv2.THRESH_BINARY_INV)
        self.original_mask_inv = cv2.bitwise_not(self.original_mask)

    def toggle_filter(self):
        if self.filter_bool:
            self.filter_bool = False
        else:
            self.filter_bool = True

    def get_frame(self):
        if self.vid.isOpened():
            self.ret, frame = self.vid.read()

            if self.filter_bool is True:
                frame = self.apply_filter(frame)

            if self.ret:
                # Return a boolean success flag and the current frame converted to BGR
                return self.ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return self.ret, None
        else:
            return self.ret, None

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def apply_filter(self, frame):

        img_h, img_w = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # find faces in image using classifier
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        # for every face found:
        for (x, y, w, h) in faces:

            # coordinates of face region
            face_w = w
            face_h = h
            face_x1 = x
            face_x2 = face_x1 + face_w
            face_y1 = y
            face_y2 = face_y1 + face_h

            # witch size in relation to face by scaling
            witch_width = int(1.5 * face_w)
            witch_height = int(witch_width * self.original_witch_h / self.original_witch_w)

            # setting location of coordinates of witch
            witch_x1 = face_x2 - int(face_w / 2) - int(witch_width / 2)
            witch_x2 = witch_x1 + witch_width
            witch_y1 = face_y1 - int(face_h * 1.25)
            witch_y2 = witch_y1 + witch_height

            # check to see if out of frame
            if witch_x1 < 0:
                witch_x1 = 0
            if witch_y1 < 0:
                witch_y1 = 0
            if witch_x2 > img_w:
                witch_x2 = img_w
            if witch_y2 > img_h:
                witch_y2 = img_h

            # Account for any out of frame changes
            witch_width = witch_x2 - witch_x1
            witch_height = witch_y2 - witch_y1

            # resize witch to fit on face
            self.witch = cv2.resize(self.witch, (witch_width, witch_height), interpolation=cv2.INTER_AREA)
            mask = cv2.resize(self.original_mask, (witch_width, witch_height), interpolation=cv2.INTER_AREA)
            mask_inv = cv2.resize(self.original_mask_inv, (witch_width, witch_height), interpolation=cv2.INTER_AREA)

            # take ROI for witch from background that is equal to size of witch image
            roi = frame[witch_y1:witch_y2, witch_x1:witch_x2]

            # original image in background (bg) where witch is not
            roi_bg = cv2.bitwise_and(roi, roi, mask=mask)
            roi_fg = cv2.bitwise_and(self.witch, self.witch, mask=mask_inv)
            dst = cv2.add(roi_bg, roi_fg)

            # put back in original image
            frame[witch_y1:witch_y2, witch_x1:witch_x2] = dst

            return frame
