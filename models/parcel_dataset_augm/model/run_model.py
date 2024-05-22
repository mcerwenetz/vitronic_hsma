from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.models import load_model
import numpy as np
import mimetypes
import argparse
import imutils
import cv2
import os
import sys
import os

MODEL_PATH = sys.argv[1]
IMAGES_PATH = sys.argv[2]
images = os.listdir(IMAGES_PATH)

print("[INFO] loading object detector...")
model = load_model(MODEL_PATH)

for i in images:
image = load_img(IMAGES_PATH+'/'+i, target_size=(416, 416))

image = img_to_array(image) / 255.0
image = np.expand_dims(image, axis=0)

preds = model.predict(image)
(startX, startY, endX, endY) = preds
# load the input image (in OpenCV format), resize it such that it
# fits on our screen, and grab its dimensions
image = cv2.imread(IMAGES_PATH+'/'+i)
image = imutils.resize(image, width=600)
(h, w) = image.shape[:2]
# scale the predicted bounding box coordinates based on the image
# dimensions
startX = int(startX * w)
startY = int(startY * h)
endX = int(endX * w)
endY = int(endY * h)
# draw the predicted bounding box on the image
cv2.rectangle(image, (startX, startY), (endX, endY),
(0, 255, 0), 2)
# show the output image
cv2.imshow("Output", image)
