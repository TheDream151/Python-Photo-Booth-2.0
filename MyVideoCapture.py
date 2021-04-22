import cv2


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
        self.filter_bool = False
        # read images
        self.beard = cv2.imread('beard.png')
        # get shape of filter
        self.original_beard_h, self.original_beard_w, self.beard_channels = self.beard.shape
        # convert to gray
        beard_gray = cv2.cvtColor(self.beard, cv2.COLOR_BGR2GRAY)
        # create mask and inverse mask of filter
        ret, self.original_beard_mask = cv2.threshold(beard_gray, 10, 255, cv2.THRESH_BINARY_INV)
        self.original_beard_mask_inv = cv2.bitwise_not(self.original_beard_mask)

        self.hat = cv2.imread('hat.png')
        # get shape of filter
        self.original_hat_h, self.original_hat_w, self.hat_channels = self.hat.shape
        # convert to gray
        hat_gray = cv2.cvtColor(self.hat, cv2.COLOR_BGR2GRAY)
        # create mask and inverse mask of filter
        ret, self.original_hat_mask = cv2.threshold(hat_gray, 10, 255, cv2.THRESH_BINARY_INV)
        self.original_hat_mask_inv = cv2.bitwise_not(self.original_hat_mask)

    def toggle_filter(self):
        """
        Toggles the filter displaying in the camera feed
        """
        if self.filter_bool:
            self.filter_bool = False
        else:
            self.filter_bool = True

    def get_frame(self):
        """
        Retrieves the current camera feed
        """

        ret = False
        if self.vid.isOpened():
            ret, frame = self.vid.read()

            if self.filter_bool is True:
                # self.apply_hat_filter(frame)
                self.__apply_filter(frame)

            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return ret, None

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def __apply_filter(self, frame):
        """
        Applies the filter to the current camera feed
        @:param frame this is the frame that the filter is added to
        """
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

            # filter size in relation to face by scaling
            filter_width = int(face_w)
            filter_height = int(filter_width * self.original_beard_h / self.original_beard_w)

            # setting location of coordinates of filter
            filter_x1 = face_x2 - int(face_w / 2) - int(filter_width / 2)
            filter_x2 = filter_x1 + filter_width
            filter_y1 = face_y1 + int(face_h / 1.75)
            filter_y2 = filter_y1 + int(filter_height / 1.75)

            # check to see if out of frame
            if filter_x1 < 0:
                filter_x1 = 0
            if filter_y1 < 0:
                filter_y1 = 0
            if filter_x2 > img_w:
                filter_x2 = img_w
            if filter_y2 > img_h:
                filter_y2 = img_h

            # Account for any out of frame changes
            filter_width = filter_x2 - filter_x1
            filter_height = filter_y2 - filter_y1

            # resize filter to fit on face
            self.beard = cv2.resize(self.beard, (filter_width, filter_height), interpolation=cv2.INTER_AREA)
            mask = cv2.resize(self.original_beard_mask, (filter_width, filter_height), interpolation=cv2.INTER_AREA)
            mask_inv = cv2.resize(self.original_beard_mask_inv, (filter_width, filter_height),
                                  interpolation=cv2.INTER_AREA)

            # take ROI for filter from background that is equal to size of filter image
            roi = frame[filter_y1:filter_y2, filter_x1:filter_x2]
            # original image in background (bg) where filter is not
            roi_bg = cv2.bitwise_and(roi, roi, mask=mask)
            roi_fg = cv2.bitwise_and(self.beard, self.beard, mask=mask_inv)
            dst = cv2.add(roi_bg, roi_fg)

            # put back in original image
            frame[filter_y1:filter_y2, filter_x1:filter_x2] = dst

            # filter size in relation to face by scaling
            filter_width = int(1.4 * face_w)
            filter_height = int(filter_width * self.original_hat_h / self.original_hat_w)

            # setting location of coordinates of filter
            filter_x1 = face_x2 - int(face_w / 2) - int(filter_width / 2)
            filter_x2 = filter_x1 + filter_width
            filter_y1 = face_y1 - int(face_h * 1.25)
            filter_y2 = filter_y1 + int(filter_height * 1.25)

            # check to see if out of frame
            if filter_x1 < 0:
                filter_x1 = 0
            if filter_y1 < 0:
                filter_y1 = 0
            if filter_x2 > img_w:
                filter_x2 = img_w
            if filter_y2 > img_h:
                filter_y2 = img_h

            # Account for any out of frame changes
            filter_width = filter_x2 - filter_x1
            filter_height = filter_y2 - filter_y1

            # resize filter to fit on face
            self.hat = cv2.resize(self.hat, (filter_width, filter_height), interpolation=cv2.INTER_AREA)
            mask = cv2.resize(self.original_hat_mask, (filter_width, filter_height), interpolation=cv2.INTER_AREA)
            mask_inv = cv2.resize(self.original_hat_mask_inv, (filter_width, filter_height),
                                  interpolation=cv2.INTER_AREA)

            # take ROI for filter from background that is equal to size of filter image
            roi = frame[filter_y1:filter_y2, filter_x1:filter_x2]

            # original image in background (bg) where filter is not
            roi_bg = cv2.bitwise_and(roi, roi, mask=mask)
            roi_fg = cv2.bitwise_and(self.hat, self.hat, mask=mask_inv)
            dst = cv2.add(roi_bg, roi_fg)

            # put back in original image
            frame[filter_y1:filter_y2, filter_x1:filter_x2] = dst
