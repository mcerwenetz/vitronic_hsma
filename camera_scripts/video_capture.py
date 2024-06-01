import numpy as np
import cv2
import picamera2

MAX_ACTIVITY_RATION_THRESHOLD = 0.2
LEARN_ITERATIONS=20

def learn_mask(background_subtractor, camera):
    print("learning")
    max_activity = 0
    for _ in range(LEARN_ITERATIONS):
        im = camera.capture_array()
        fgmask = background_subtractor.apply(im)
        current_activity = np.count_nonzero(fgmask)
        if current_activity > max_activity:
            max_activity = current_activity
    print("finished learning")
    return max_activity

def check_activity(background_subtractor, camera, max_activity):
    while(True):
        im = camera.capture_array()
        fgmask = background_subtractor.apply(im)
        current_activity = np.count_nonzero(fgmask)
        print(current_activity)
        if current_activity > max_activity*MAX_ACTIVITY_RATION_THRESHOLD:
            print("activity detected")



def main():
    camera = picamera2.Picamera2()
    camera.configure(camera.create_preview_configuration(
        main={"format": 'XRGB8888', "size": (3780, 2464)}))
    camera.set_controls({"ExposureTime": 1000})
    camera.start()
    background_subtractor = cv2.bgsegm.createBackgroundSubtractorCNT()
    max_activity = learn_mask(background_subtractor, camera)
    check_activity(background_subtractor, camera, max_activity)


if __name__ == '__main__':
    main()