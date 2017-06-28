import pyueye
import time

cam = pyueye.uEyeCAM()
cam.set_ImageFormat("640x480")

while True :
    local_img = cam.snap()
    local_img.show()

    # display image for 10 seconds
    #time.sleep(1)