import cv2
import numpy as np

path = "first_try/"
bg_removed_path = "bg_rem/"

fgbg = cv2.bgsegm.createBackgroundSubtractorCNT()


print("learning")
# mask training
max_activity = 0
for _ in range(30):
    im = cv2.imread(f"{path}{0}.jpg")
    fgmask = fgbg.apply(im)
    current_activity = np.count_nonzero(fgmask)
    if current_activity > max_activity:
        max_activity = current_activity

print("finished learning")

# detect
for i in range(30):
    fgmask = fgbg.apply(im)
    im = cv2.imread(f"{path}{i}.jpg")
    current_activity = np.count_nonzero(fgmask)
    if current_activity > max_activity*0.4:
        print(f"detected activity in picture {i}.jpg")
        print(f"current activity: {current_activity}")
        im_without_bg = cv2.bitwise_and(last_im, last_im, mask=fgmask)
        cv2.imwrite(f"{bg_removed_path}{i}.jpg",im_without_bg)
        cv2.imwrite(f"{bg_removed_path}{i}_mask.jpg",fgmask)
    last_im = im
    i+=1
