import picamera2
from time import sleep, time

import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import inference

MAX_ACTIVITY_RATION_THRESHOLD = 0.4
bg_removed_path = "bg_rem/"


def learn_mask():
    print("learning")
    fgbg = cv2.bgsegm.createBackgroundSubtractorCNT()
    max_activity = 0
    for _ in range(30):
        im = cv2.imread(f"{0}.jpg")
        fgmask = fgbg.apply(im)
        current_activity = np.count_nonzero(fgmask)
        if current_activity > max_activity:
            max_activity = current_activity
    print("finished learning")
    return fgbg, max_activity


def check_activity(fgbg, image, max_activity):
    fgmask = fgbg.apply(image)
    current_activity = np.count_nonzero(fgmask)
    if current_activity > max_activity*MAX_ACTIVITY_RATION_THRESHOLD:
        return True, fgmask
    else:
        return False, False


def main():

    camera = picamera2.Picamera2()
    camera.configure(camera.create_preview_configuration(
        main={"format": 'XRGB8888', "size": (3780, 2464)}))
    # Exposure time. 100 = 1 ms
    camera.set_controls({"ExposureTime": 1000})
    model = inference.get_model("classification-ofjuw/3")

    camera.start()

    if sys.argv[1]:
        # argv = Hz, gets calculated to seconds for sleeping
        shutter_speed = 1 / int(sys.argv[1])
    else:
        shutter_speed = 1 / 24

    if sys.argv[1]:
        num_pics = int(sys.argv[2])
    else:
        num_pics = 100

    # taking images
    input("press for shutter")

    for i in range(num_pics):
        img = camera.capture_image()
        img.save(f"{i}.jpg")

        i += 1
        sleep(shutter_speed)

    # fgbg,max_activity = learn_mask()

    for i in range(num_pics):
        ts1 = time()
        # im = cv2.imread(f"{i}.jpg")
        # activity_happend, mask = check_activity(fgbg, im, max_activity)
        result = (model.infer(image=f"{i}.jpg"))

        # if activity_happend == True:
        #    print("anomaly detected")
        #    im_without_bg = cv2.bitwise_and(im, im, mask=mask)
        #    cv2.imwrite(f"{bg_removed_path}{i}.jpg",im_without_bg)
        print(result)
        ts2 = time()

        print((ts2-ts1))


if __name__ == "__main__":
    main()
