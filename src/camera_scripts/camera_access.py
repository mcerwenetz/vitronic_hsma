from picamera2 import Picamera2

from time import sleep

camera = Picamera2()

camera.start()

sleep(2)

camera.capture_file("image.jpg")