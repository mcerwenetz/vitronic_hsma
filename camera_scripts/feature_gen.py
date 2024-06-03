import numpy as np
import cv2
import picamera2
from time import sleep, time
import matplotlib.pyplot as plt
import sys
import inference
import serial

MAX_ACTIVITY_RATION_THRESHOLD = 0.4
LEARN_ITERATIONS=20

ser = serial.Serial('/dev/ttyACM0', 115200, timeout = 1)

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
        return index, fg_list[index]     

def main():
    
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
    print("[INFO] waiting for package")
    current_activity = 0 
    while(True):
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
                print("[INFO] Finished classification and feature detection")
                print("[INFO] Results: ")
                print(f"[INFO] Classification: {result[0].predicted_classes}")
                print(f"[INFO] Features: {des}")
                print(f"[INFO] classification and feature detection took {ts_fc_1-ts_fc_0} s")
                img_list = []


if __name__ == "__main__":
    main()
