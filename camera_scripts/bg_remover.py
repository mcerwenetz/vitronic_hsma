import cv2

ims = [cv2.imread(f"{i}.jpg") for i in range(18)]

fgbg = cv2.bgsegm.createBackgroundSubtractorCNT()

for im in ims:
    fgmask = fgbg.apply(im)

skateboard= cv2.imread("19.jpg")
mask = fgbg.apply(skateboard)

skateboard = cv2.bitwise_and(skateboard, skateboard, mask=mask)

cv2.imwrite("bg_rem.jpg", skateboard) 