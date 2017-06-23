import pyueye
import time
import psutil

cam = pyueye.uEyeCAM()
cam.set_ImageFormat("640x480")


while True :
    cam.get_img()
    # display image for 10 seconds
    #time.sleep(1)

    # hide image
    for proc in psutil.process_iter():
        if proc.name() == "display":
            proc.kill()