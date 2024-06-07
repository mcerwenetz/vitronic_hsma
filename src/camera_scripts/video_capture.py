import numpy as np
import cv2
<<<<<<< HEAD
import picamera2
# import time

MAX_ACTIVITY_RATION_THRESHOLD = 0.3
LEARN_ITERATIONS=20

def learn_mask(background_subtractor, camera):
    print("learning")
    max_activity = 0
    for _ in range(LEARN_ITERATIONS):
        im = camera.capture_array()
        fgmask = background_subtractor.apply(im)
=======

MAX_ACTIVITY_RATION_THRESHOLD = 0.4

def learn_mask():
    print("learning")
    fgbg = cv2.bgsegm.createBackgroundSubtractorCNT()
    max_activity = 0
    for _ in range(30):
        im = cv2.imread(f"{0}.jpg")
        fgmask = fgbg.apply(im)
>>>>>>> master
        current_activity = np.count_nonzero(fgmask)
        if current_activity > max_activity:
            max_activity = current_activity
    print("finished learning")
<<<<<<< HEAD
    return max_activity

def check_activity(background_subtractor, camera, max_activity, orb):
    while(True):
        im = camera.capture_array()
        fgmask = background_subtractor.apply(im)
        current_activity = np.count_nonzero(fgmask)
        if current_activity > max_activity*MAX_ACTIVITY_RATION_THRESHOLD:
            print("activity detected")
            im = cv2.bitwise_and(im, im, mask=fgmask)
            im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            kp, des = orb.detectAndCompute(im, None)
            # im = cv2.drawKeypoints(im, kp, None, color=(0,255,0), flags=None)
            # cv2.imwrite("detected_image.jpg",im)
            print(des)


def main():
    camera = picamera2.Picamera2()
    camera.configure(camera.create_preview_configuration(
        main={"format": 'XRGB8888', "size": (3780, 2464)}))
    camera.set_controls({"ExposureTime": 1000})
    camera.start()
    orb = cv2.ORB.create()

    background_subtractor = cv2.bgsegm.createBackgroundSubtractorCNT()
    max_activity = learn_mask(background_subtractor, camera)
    check_activity(background_subtractor, camera, max_activity, orb)


if __name__ == '__main__':
    main()
=======
    return fgbg, max_activity

def run(fgbg, cap, max_activity):
    while(True):
        ret, frame = cap.read()
        fgmask = fgbg.apply(frame)
        current_activity = np.count_nonzero(fgmask)
        if current_activity > max_activity*MAX_ACTIVITY_RATION_THRESHOLD:
            print("activity detected")



def main():
    cap = cv2.VideoCapture('vtest.avi')
    fgbg, max_activity = learn_mask()
    run(fgbg, cap, max_activity)
>>>>>>> master
