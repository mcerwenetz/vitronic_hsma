import numpy as np
import cv2

MAX_ACTIVITY_RATION_THRESHOLD = 0.4

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
