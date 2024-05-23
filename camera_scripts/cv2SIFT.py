from picamera2 import Picamera2
from time import sleep

import cv2
import sys

def main():
    if len(sys.argv) < 1:
        print("please provide filename to safe final file")
        return
    filename = sys.argv[1]
    camera = Picamera2()
    camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
    camera.start()

    sleep(2)

    img = camera.capture_array()
    gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT.create()
    keypoints = sift.detect(gray)

    img = cv2.drawKeypoints(gray, keypoints, img)

    cv2.imwrite(filename, img)



if __name__ == "__main__":
    main()