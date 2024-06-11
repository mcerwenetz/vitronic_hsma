from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.models import load_model
import tensorflow as tf
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
#images.remove("_annotations.csv")
print("[INFO] loading object detector...")

#model = tf.saved_model.load(MODEL_PATH)
model = tf.keras.models.load_model(MODEL_PATH)
#model=tf.keras.layers.TFSMLayer(MODEL_PATH, call_endpoint='serving_default')

for i in images:
    image = load_img(IMAGES_PATH+'/'+i, target_size=(224, 224))

    image = img_to_array(image) / 255.0
    image = np.expand_dims(image, axis=0)

    preds = model.predict(image)
    bbox_list = preds
    startX = bbox_list[0][0]
    startY = bbox_list[0][1]
    endX = bbox_list[0][2]
    endY = bbox_list[0][3]
    
    # (startX, startY, endX, endY) = preds
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
    # cropped_image = image[Y:startY+endY, X:startX+endX]
    # plt.imshow(cropped_image)
    # show the output image
    cv2.imshow("Output", image)
    cv2.waitKey(0)
