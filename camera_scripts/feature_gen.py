import PIL.Image
import numpy as np
import cv2
import picamera2
from time import sleep, time
import matplotlib.pyplot as plt
import sys
import inference
import serial
import PIL

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

    while(True):
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if line == "interrupted light barrier":
                for i in range(num_pics):
                    ts1 = time()
                    img = camera.capture_array()
                    img_list.append(img)
                    i+=1
                    sleep(shutter_speed)
                    ts2 = time()
                    ts = (ts2-ts1)
                for e,i in enumerate(img_list):
                    img = PIL.Image.fromarray(i)
                    img.save(f"{e}.png")
            else:
                vals = line.split(" ")
                print(f"[INFO] interrupt time {vals[0]} ms")
                print(f"[INFO] taking pictures took: {(ts)} s")
                used_image = int(int(vals[0])/(ts * 1000)) +1
                print(f"[INFO] used image: {used_image}")
                
                print("[INFO] Starting classification and feature detection")
                ts_fc_0 = time()
                fgmask = background_subtractor.apply(img_list[used_image])
                im = cv2.bitwise_and(img_list[used_image], img_list[used_image], mask=fgmask)
                im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                kp, des = orb.detectAndCompute(im, None)
                #im = PIL.Image.fromarray(i)
                result = (model.infer(image=f"{used_image}.png"))
                ts_fc_1 = time()
                print("[INFO] Finished classification and feature detection")
                print("[INFO] Results: ")
                print(f"[INFO] Classification: {result[0].predicted_classes}")
                print(f"[INFO] Features: {des}")
                print(f"[INFO] classification and feature detection took {ts_fc_1-ts_fc_0} s")
                img_list = []


if __name__ == "__main__":
    main()
