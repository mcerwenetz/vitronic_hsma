import cv2
import numpy as np
from time import sleep

path = "first_try/"
bg_removed_path = "bg_rem/"

fgbg = cv2.bgsegm.createBackgroundSubtractorCNT()


print("learning")
# mask traiing
max_activity = 0
for _ in range(30):
    im = cv2.imread(f"{path}{0}.jpg")
    fgmask = fgbg.apply(im)
    current_activity = np.count_nonzero(fgmask)
    if current_activity > max_activity:
        max_activity = current_activity

print("finished learning")

firsttime = True
# detect
for i in range(30):
    fgmask = fgbg.apply(im)
    im = cv2.imread(f"{path}{i}.jpg")
    current_activity = np.count_nonzero(fgmask)
    if current_activity > max_activity*0.4:
        print(f"detected activity in picture {i}.jpg")
        print(f"current activity: {current_activity}")
        if firsttime == True:
            old_fgmask = fgmask
            firsttime = False
            continue
        else:
            im_without_bg = cv2.bitwise_and(im, im, mask=old_fgmask)
            cv2.imwrite(f"{bg_removed_path}{i}.jpg",im_without_bg)
            old_fgmask = fgmask
    i+=1

# skateboard= cv2.imread("19.jpg")
# mask = fgbg.apply(skateboard)
# 
# skateboard = cv2.bitwise_and(skateboard, skateboard, mask=mask)
# 
# cv2.imwrite("bg_rem.jpg", skateboard) 