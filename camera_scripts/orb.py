from picamera2 import Picamera2, Preview
from time import sleep, time

import cv2
import matplotlib.pyplot as plt


def main():

    camera = Picamera2()
    camera.configure(camera.create_preview_configuration(
        main={"format": 'XRGB8888', "size": (1920, 1080)}))
    camera.start_preview()
    camera.start()

    input("press enter for first photo")

    img = camera.capture_array()


    input("press enter for second photo")
    img2 = camera.capture_array()
    start = time()

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB.create()
    # find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors.
    matches = bf.match(des1, des2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key=lambda x: x.distance)

    end = time()

    print(f"elapsed time: {end-start}")

    # Draw first 10 matches.
    img3 = cv2.drawMatches(
        img, kp1, img2, kp2, matches[:20], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    plt.imshow(img3), plt.show()


if __name__ == "__main__":
    main()
