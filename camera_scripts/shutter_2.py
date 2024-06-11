import picamera2
from time import sleep, time

import cv2
import matplotlib.pyplot as plt
import sys
import inference



def main():

    camera = picamera2.Picamera2()
    camera.configure(camera.create_preview_configuration(
        main={"format": 'XRGB8888', "size": (3780,2464)}))
    # Exposure time. 100 = 1 ms
    camera.set_controls({"ExposureTime":1000})
    model = inference.get_model("classification-ofjuw/1")

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

    

    for i in range(num_pics):
        input("press for shutter")
        img = camera.capture_image()
        img.save(f"{i}.jpg")
        
        i+=1
        sleep(shutter_speed)
    for i in range(num_pics):
        ts1 = time()
        result = (model.infer(image=f"{i}.jpg"))
        ts2 = time()
        print(result)
        print((ts2-ts1))



if __name__ == "__main__":
    main()
