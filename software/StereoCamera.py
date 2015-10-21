import cv2
import numpy as np
import time

__author__ = 'def'

class StereoCamera:

    class CameraError(BaseException):
        pass

    webcam_resolution = (640, 480)
    viewer_resolution = (1920, 1080)

    def __init__(self, left_camera_device='/dev/video1', right_camera_device='/dev/video2',
                       left_camera_inverted = False, right_camera_inverted = True):
        self.left_camera_device = left_camera_device
        self.right_camera_device = right_camera_device

        self.left_camera_inverted = left_camera_inverted
        self.right_camera_inverted = right_camera_inverted

        self.left_camera = None
        self.right_camera = None
        self.init_cameras()

        self.left_picture = None
        self.right_picture = None

    def __del__(self):
        self.left_camera.release()
        self.right_camera.release()

    def init_cameras(self):
        self.left_camera = cv2.VideoCapture(1)
        self.left_camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 800)
        self.left_camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
        # left_camera.open()
        self.right_camera = cv2.VideoCapture(2)
        self.right_camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 800)
        self.right_camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
        # right_camera.open()

        if not self.left_camera.isOpened():
            raise StereoCamera.CameraError("Error opening left camera")
        if not self.right_camera.isOpened():
            raise StereoCamera.CameraError("Error opening right camera")

        self.camera_startup()

    def camera_startup(self):
        tries = 0
        while tries < 10:
            l_status, dummy = self.left_camera.read()
            r_status, dummy = self.right_camera.read()

            if l_status and r_status:
                break
            else:
                tries += 1
        else:
            raise StereoCamera.CameraError("Timeout reading cameras")


    def capture_stereo_pair(self):
        l_status = self.left_camera.grab()
        r_status = self.right_camera.grab()

        if not l_status:
            print "Left camera error (grabbing)"
        if not r_status:
            print "Right camera error (grabbing)"


        l_status, self.left_picture = self.left_camera.retrieve()
        r_status, self.right_picture = self.right_camera.retrieve()

        if not l_status:
            print "Left camera error (retrieve)"
        if not r_status:
            print "Right camera error (retrieve)"

        return self.left_picture, self.right_picture

    def get_stereo_image(self):
        self.left_picture, self.right_picture = self.capture_stereo_pair()
        rotated_right = np.rot90(self.right_picture, 2)
        # cv2.imshow('Left image', left_picture)
        #cv2.imshow('Right image', rotated_right)

        # Scale images
        factor = self.viewer_resolution[1] / float(self.webcam_resolution[1])
        left_resized = cv2.resize(self.left_picture, None, fx=factor, fy=factor, interpolation=cv2.INTER_CUBIC)
        right_resized = cv2.resize(rotated_right, None, fx=factor, fy=factor, interpolation=cv2.INTER_CUBIC)

        # Calculate optic axis (Approximately)
        left_center = (left_resized.shape[0] / 2, left_resized.shape[1] / 2)
        right_center = (right_resized.shape[0] / 2, right_resized.shape[1] / 2)

        # Concatenate images (based on optical center):
        half_size_eye = self.viewer_resolution[0] / 4
        combined_image = np.concatenate((self.left_picture[:, left_center[0] - half_size_eye:left_center[0] + half_size_eye, :],
                                         rotated_right[:, right_center[0] - half_size_eye:right_center[0] + half_size_eye,
                                         :]),
                                        axis=1)
        return combined_image
