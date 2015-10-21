import cv2
import numpy as np
import time

import StereoCamera

__author__ = 'def'

record_video = False

def main():
    stereoCam = StereoCamera.StereoCamera()

    if record_video:
        # Video output
        writer = cv2.VideoWriter(time.strftime("stereo-%d_%m_%y-%H_%M_%S.avi"), cv2.cv.FOURCC('M','J','P','G'), 25, (1160,480))


    while True:
        combined_image = stereoCam.get_stereo_image()

        cv2.imshow('Stereo pair', combined_image)

        user_input = cv2.waitKey(1) & 0xFF
        if user_input == ord('q'):
            break
        elif user_input == ord('c'):
            cv2.imwrite(time.strftime("stereo-%d_%m_%y-%H_%M_%S.png"), combined_image)
            break

        if record_video:
            writer.write(combined_image)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()