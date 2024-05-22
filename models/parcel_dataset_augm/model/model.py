from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import datetime
import time

LEARNING_RATE= 1e-4
EPOCHS = 10
BATCH_SIZE = 32
DENSE_1 = 128
DENSE_2 = 64
DENSE_3 = 32
DENSE_4 = 4

def get_data(rows,path):
    data = []
    targets = []
    filenames = []
    
    for row in rows[1:]:
    	# break the row into the filename and bounding box coordinates
    	row = row.split(",")
    	(filename, width, height, _class, xmin, ymin, xmax, ymax) = row
    	width = int(width)
    	height = int(height)
    	imagePath = os.path.sep.join([path, filename])
    	image = cv2.imread(imagePath)
    	# scale the bounding box coordinates relative to the spatial
    	# dimensions of the input image
    	startX = float(xmin) / width
    	startY = float(ymin) / height
    	endX = float(xmax) / width
    	endY = float(ymax) / height
    
    	
    	image = load_img(imagePath, target_size=(width, height))
    	image = img_to_array(image)
    	# update our list of data, targets, and filenames
    	data.append(image)
    	targets.append((startX, startY, endX, endY))
    	filenames.append(filename)
    	
    data = np.array(data, dtype="float32") / 255.0
    targets = np.array(targets, dtype="float32")
    	
    return data,targets,filenames

TEST_PATH = "/home/ela/Desktop/vitronic/parcel_dataset_augm/test/"
VALID_PATH = "/home/ela/Desktop/vitronic/parcel_dataset_augm/valid/"
TRAIN_PATH = "/home/ela/Desktop/vitronic/parcel_dataset_augm/train/"

print("[INFO] loading dataset...")
rows_test = open(TEST_PATH+"_annotations.csv").read().strip().split("\n")
rows_valid = open(VALID_PATH+"_annotations.csv").read().strip().split("\n")
rows_train = open(TRAIN_PATH+"_annotations.csv").read().strip().split("\n")

# initialize the list of data (images), our target output predictions
# (bounding box coordinates), along with the filenames of the
# individual images

train_data,train_targets,train_filenames = get_data(rows_train,TRAIN_PATH)
valid_data,valid_targets,valid_filenames = get_data(rows_valid,VALID_PATH)
test_data,test_targets,test_filenames = get_data(rows_test,TEST_PATH)

vgg = VGG16(weights="imagenet", include_top=False,
	input_tensor=Input(shape=(416, 416, 3)))
# freeze all VGG layers so they will *not* be updated during the
# training process
vgg.trainable = False
# flatten the max-pooling output of VGG
flatten = vgg.output
flatten = Flatten()(flatten)
# construct a fully-connected layer header to output the predicted
# bounding box coordinates
bboxHead = Dense(DENSE_1, activation="relu")(flatten)
bboxHead = Dense(DENSE_2, activation="relu")(bboxHead)
bboxHead = Dense(DENSE_3, activation="relu")(bboxHead)
bboxHead = Dense(DENSE_4, activation="sigmoid")(bboxHead)
# construct the model we will fine-tune for bounding box regression
model = Model(inputs=vgg.input, outputs=bboxHead)

opt = Adam(learning_rate=LEARNING_RATE)
model.compile(loss="mse", optimizer=opt, metrics=['accuracy'])
print(model.summary())
# train the network for bounding box regression
print("[INFO] training bounding box regressor...")
H = model.fit(
	train_data, train_targets,
	validation_data=(valid_data, valid_targets),
	batch_size=BATCH_SIZE,
	epochs=EPOCHS,
	callbacks=EarlyStopping(verbose=1, patience=2),
	verbose=1)
	
print("[INFO] saving object detector model...")
ts = time.time()
model_name = "model"+datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
model.save("/home/ela/Desktop/vitronic/parcel_dataset_augm/"+model_name)
# plot the model training history
N = len(H.history["loss"])
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
plt.title("Bounding Box Regression Loss on Training Set")
plt.xlabel("Epoch #")
plt.ylabel("Loss")
plt.legend(loc="lower left")
plt.savefig("/home/ela/Desktop/vitronic/parcel_dataset_augm/"+model_name+"/training_plot.png")
