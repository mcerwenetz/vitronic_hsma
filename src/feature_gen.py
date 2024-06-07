import os
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
from multiprocessing.pool import ThreadPool
import socket

MAX_ACTIVITY_RATION_THRESHOLD = 0.4
LEARN_ITERATIONS=200
GATE=0
IP="0.0.0.0"
PORT="8080"
USED_IMAGE=5
orb_feats = 500

ser = serial.Serial('/dev/ttyACM0', 115200, timeout = 1)

def setup_db():
    connection = psycopg2.connect(dbname="vitronicdb", user="vitronic",
                                  password="vitronicpasswd", host="141.19.96.152", port="5432")
    cursor = connection.cursor()
    return connection,cursor

def send_image(image_path,client_socket):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    image_length = len(image_data)
    image_length_bytes = image_length.to_bytes(4, 'big')

    client_socket.sendall(image_length_bytes + image_data)

def send_array(image_path,client_socket):
    image = cv2.imread(image_path)
    _, image_encoded = cv2.imencode('.jpg', image)
    array_data = image_encoded.tobytes()
    array_length = len(array_data)
    array_length_bytes = array_length.to_bytes(4, 'big')

    client_socket.sendall(array_length_bytes + array_data)

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

def create_fgmask(background_subtractor,i):
        print("[INFO] getting best picture")
        i = np.array(i)
        fgmask = background_subtractor.apply(i)
        #np.count_nonzero(fgmask)

        return fgmask     

def cl_model_func(model,im):
    print("[INFO] Starting classification")
    result = (model.infer(image=im))

    return result[0].predicted_classes[0]


def orb_func(orb,im,fgmask):
    im = np.array(im)
    im = cv2.bitwise_and(im,im, mask=fgmask)
    # im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f"orb_{GATE}.jpg",im)
    send_image.send_image(f"orb_{GATE}.jpg",IP,PORT)
    kp, des = orb.detectAndCompute(im, None)
    return des



def main():
    expt = input("Enter Exposure Time (100 = 1ms)")

    print("[INFO] connecting to socket")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client_socket.connect((IP,PORT))

    #os.system('export ROBOFLOW_API_KEY="5BBeWc9fVb0WznH4RnJn"')
    print("[INFO] starting database setup")
    connection, db_cursor = setup_db()

    print("[INFO] starting camera setup")
    camera = picamera2.Picamera2()
    camera.configure(camera.create_preview_configuration(
        main={"format": 'YUV420', "size": (3780, 2464)}))
    # Exposure time. 100 = 1 ms
    camera.set_controls({"ExposureTime":500})
    camera.start()
    
    print("[INFO] starting model setup")
    model = inference.get_model("classification-ofjuw/3")


    print("[INFO] learning mask")
    background_subtractor = cv2.bgsegm.createBackgroundSubtractorCNT()
    max_activity = learn_mask(background_subtractor, camera)

    print("[INFO] setting up orb")
    orb = cv2.ORB.create(orb_feats)
    

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
    print("[INFO] waiting for packages")
    pc = 0
    pool  = ThreadPool(processes=2)

    des_list = []

    while(True):
        if ser.in_waiting > 0:
            print("[INFO] package detected")

            client_socket.connect((IP,PORT))
            print("[INFO] connected")

            total_time_0 = time() 
            
            pc +=1
            # os.makedirs(f"{pc}_data",exist_ok=True)
            img_list = []
            ts1 = time()
            for i in range(num_pics):
                img = camera.capture_image()
                img_list.append(img)
                i+=1
                sleep(shutter_speed)
            ts2 = time()
            ts = (ts2-ts1)
            for e,i in enumerate(img_list):
                i.save(f"{pc}_{e}.jpg")

            send_image(f"{pc}_{USED_IMAGE}{GATE}.jpg",client_socket)

            

            fgmask = create_fgmask(background_subtractor,img_list[USED_IMAGE])

            orb_calc = orb_func(orb,f"{pc}_{USED_IMAGE}.jpg",fgmask)
            send_image(f"{pc}_{USED_IMAGE}_orb.jpg",client_socket)
            send_array(f"{pc}_{USED_IMAGE}_orb.jpg",client_socket)



            client_socket.close()

                # status = 1
                # print(f"[INFO] interrupt time {vals[0]} ms")
                # print(f"[INFO] taking pictures took: {(ts)} s")
                
                # ts_fc_0 = time()

                # used_image, fgmask = get_best_picture(background_subtractor,img_list)

                # pool  = ThreadPool(processes=2)

                # orb_calc = pool.apply_async(orb_func,args=(orb,img_list[used_image],fgmask))
                # cl_calc = pool.apply_async(cl_model_func, args=(model,img_list[used_image]))

                # orb_result = orb_calc.get()
                # cl_result = cl_calc.get()
                
                # des_list.append(orb_result)

                # ts_fc_1 = time()

                # features = {"gate":0,"feature_vector":des,"classifictaion":cl_result[0].predicted_classes[0]}

                # if cl_result == "bad":
                #     status = 2

                # print()
                # print("[INFO] Finished classification and feature detection")
                # print("[INFO] Results: ")
                # print()
                # print(f"[INFO] Gate: 0")
                # print(f"[INFO] Classification: {cl_result}")
                # print(f"[INFO] Feature Vector: {orb_result}")
                # print()
                # print(f"[INFO] classification and feature detection took {ts_fc_1-ts_fc_0} s")
                # sql_funcs.addEntry(connection,db_cursor,GATE,status,orb_result,orb_result.shape)
                # print("[INFO] database query was send")
                # print(f"[INFO] total time  {ts_fc_1-total_time_0} s")

if __name__ == "__main__":
    main()
