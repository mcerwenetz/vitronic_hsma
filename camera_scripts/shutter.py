import picamera2
from time import sleep, time
import serial
import cv2
import matplotlib.pyplot as plt
import sys
import inference
import os

ser = serial.Serial('/dev/ttyACM0', 115200, timeout = 1)

def main():

    camera = picamera2.Picamera2()
    camera.configure(camera.create_preview_configuration(
        main={"format": 'XRGB8888', "size": (2048,2048)}))
    # Exposure time. 100 = 1 ms
    camera.set_controls({"ExposureTime":500})
    model = inference.get_model("classification-ofjuw/3")

    camera.start()

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
    while(True):
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if line == "interrupted light barrier":
                for i in range(num_pics):
                    ts1 = time()
                    img = camera.capture_image()
                    img_list.append(img)
                    i+=1
                    sleep(shutter_speed)
                    ts2 = time()
                    ts = (ts2-ts1)
                for e,i in enumerate(img_list):
                    i.save(f"{e}.jpg")
                img_list = []
            else:
                vals = line.split(" ")
                print(f"interrupt time {vals[0]}")
                print(f"taking pictures took: {(ts)}")
                used_image = int(int(vals[0])/(ts * 1000)) +1
                print(used_image)
                result = (model.infer(image=f"{used_image}.jpg"))
                print(result[0].predicted_classes)
#    for i in range(num_pics):
 #       ts1 = time()
  #      
   #     ts2 = time()
    #    
     #   print((ts2-ts1))



if __name__ == "__main__":
    main()
