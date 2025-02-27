from picamera2 import Picamera2


def main():

    camera = Picamera2()
    camera.configure(camera.create_preview_configuration(
        main={"format": 'XRGB8888', "size": (1920, 1080)}))
    camera.start_preview()
    camera.start()
    i = 0
    while True:

        inp = input("press enter to take a photo. press e to exit.")
        if inp == "e":
            break
        img = camera.capture_image()
        img.save(f"{i}.jpg")
        i+=1



if __name__ == "__main__":
    main()
