import numpy as np
import cv2
import picamera2
from time import sleep, time
import matplotlib.pyplot as plt
import sys
import inference
import serial
import psycopg2
import sql_funcs
import threading

MAX_ACTIVITY_RATION_THRESHOLD = 0.4
LEARN_ITERATIONS=20

ser = serial.Serial('/dev/ttyACM0', 115200, timeout = 1)

def setup_db():
    connection = psycopg2.connect(dbname="vitronicdb", user="vitronic",
                                  password="vitronicpasswd", host="141.19.96.152", port="5432")
    cursor = connection.cursor()
    return connection,cursor

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

def get_best_picture(background_subtractor,img_list):
        print("[INFO] getting best picture")

        tmp_list = []
        fg_list = []
        for e,i in enumerate(img_list):
            i = np.array(i)
            fgmask = background_subtractor.apply(i)
            fg_list.append(fgmask)
            tmp_list.append(np.count_nonzero(fgmask))

        index = tmp_list.index(max(tmp_list))
        print(f"[INFO] Best picture is : {index}.jpg")

        return index, fg_list[index]     

def feature_thread_func(model,orb,line,img_list,connection,db_cursor,background_subtractor,ts):
    vals = line.split(" ")
    print(f"[INFO] interrupt time {vals[0]} ms")
    print(f"[INFO] taking pictures took: {(ts)} s")
    used_image, fgmask = get_best_picture(background_subtractor,img_list)
    print("[INFO] Starting classification and feature detection")
    ts_fc_0 = time()
    im = np.array(img_list[used_image])
    im = cv2.bitwise_and(im,im, mask=fgmask)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    kp, des = orb.detectAndCompute(im, None)
    result = (model.infer(image=img_list[used_image]))
    ts_fc_1 = time()
    features = {"gate":0,"feature_vector":des,"classifictaion":result[0].predicted_classes[0]}

    if result[0].predicted_classes[0] == "bad":
        status = 0


    print("[INFO] Finished classification and feature detection")
    print("[INFO] Results: ")
    print()
    print(f"[INFO] Gate: 0")
    print(f"[INFO] Classification: {result[0].predicted_classes[0]}")
    print(f"[INFO] Feature Vector: {des}")
    print()
    print(f"[INFO] classification and feature detection took {ts_fc_1-ts_fc_0} s")
    print("[INFO] sending querry to database")
    sql_funcs.addEntry(connection,db_cursor,0,status)
    print("[INFO] finished sending querry to database")

def main():
    print("[INFO] initiation database connection")
    connection, db_cursor = setup_db()
    print("[INFO] initiation database connection finished")
    print("[INFO] starting camera setup")
    camera = picamera2.Picamera2()
    camera.configure(camera.create_preview_configuration(
        main={"format": 'XRGB8888', "size": (3780, 2464)}))
    # Exposure time. 100 = 1 ms
    camera.set_controls({"ExposureTime":1000})
    camera.start()
    print("[INFO] finished camera setup")
    
    print("[INFO] starting model setup")
    model = inference.get_model("classification-ofjuw/3")
    print("[INFO] finished model setup")


    print("[INFO] learning mask")
    background_subtractor = cv2.bgsegm.createBackgroundSubtractorCNT()
    max_activity = learn_mask(background_subtractor, camera)

    print("[INFO] setting up orb")
    orb = cv2.ORB.create()
    print("[INFO] orb setup finished")

    if sys.argv[1]:
        #argv = Hz, gets calculated to seconds for sleeping 
        shutter_speed = 1 /  int(sys.argv[1])
    else:
        shutter_speed = 1 / 24

    if sys.argv[1]:
        num_pics = int(sys.argv[2])
    else:
        num_pics = 100

    ser.reset_input_buffer()
    img_list = []
    print("[INFO] waiting for packages")
    while(True):
        status = 1
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            
            if line == "interrupted light barrier":
                ts1 = time()
                for i in range(num_pics):
                    img = camera.capture_image()
                    img_list.append(img)
                    i+=1
                    sleep(shutter_speed)
                ts2 = time()
                ts = (ts2-ts1)
                for e,i in enumerate(img_list):
                    i.save(f"{e}.jpg")
            else:

                thread = threading.Thread(target = feature_thread_func, args=(model,orb,line,img_list,connection,db_cursor,background_subtractor,ts))
                thread.start()
                img_list = []

if __name__ == "__main__":
    main()
