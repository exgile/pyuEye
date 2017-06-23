from ctypes import byref, c_int, c_char_p, c_voidp, c_char
import numpy as np
import sys
from camera_config import *
from PIL import Image
from time import sleep

class uEyeCAM :
    def __init__(self):
        # Load uEyedll file
        self.uEyeDll = ctypes.cdll.LoadLibrary("ueye_api_64.dll")

        # Handle parameters
        self.HWND = c_voidp()
        self.CAM = c_int(1)          # 1 is camera index
        self.pid = c_int()
        self.pcImgMem = c_char_p()   # create placeholder for image memory
        self.img_array = 0

        # Default RGBA
        self.width = 1280
        self.height = 720
        self.bitspixel = 32
        self.channel = 4

        # Camera Connect
        self._connect()
        print("Camera complete Ready.", file=sys.stderr)

    def _connect(self):
        nRet = 0
        nRet += self.uEyeDll.is_InitCamera(byref(self.CAM), self.HWND)
        nRet += self.uEyeDll.is_EnableAutoExit(self.CAM, c_int(0))

        # Default Format RGBA, 1280 x720
        self.set_ColorMode(mode=IS_CM_BGRA8_PACKED)
        self.set_ImageFormat("1280x720")  # Reference to camera_config.py

        if nRet == IS_SUCCESS:
            pass
        else:
            raise print("Camera connection failed.", file=sys.stderr)

    def set_ColorMode(self, mode):
        if self.uEyeDll.is_SetColorMode(self.CAM, mode) == IS_SUCCESS:
            if mode is IS_CM_BGRA8_PACKED:  # BGRA (8, 8, 8, 8)
                self.bitspixel = c_int(32)
                self.channel = 4

            elif mode is IS_CM_BGR8_PACKED:  # BGR8 (8, 8, 8)
                self.bitspixel = c_int(24)
                self.channel = 3

            elif mode is IS_CM_SENSOR_RAW8 or mode is IS_CM_MONO8:  # Gray
                self. channel = 1
                self.bitspixel = c_int(8)

            else:  # BGR565, BGR5, YCB2CY
                self.bitspixel = 16
                self.channel = 2
        else:
            print('Invalid color format', file=sys.stderr)

    def set_ImageFormat(self, res):
        if res in IMGFRMT:
            self.uEyeDll.is_ImageFormat(self.CAM, IMGFRMT_CMD_SET_FORMAT, byref(IMGFRMT[res][0]), c_int(4))
            self.width = IMGFRMT[res][1]
            self.height = IMGFRMT[res][2]

            c_width = c_int(self.width)
            c_height = c_int(self.height)

            self.uEyeDll.is_AllocImageMem(self.CAM, c_width, c_height, self.bitspixel,
                                          byref(self.pcImgMem), byref(self.pid))

            self.uEyeDll.is_SetImageMem(self.CAM, self.pcImgMem, self.pid)

            # Allocate memory :
            self.img_array = self.channel * c_char * self.width * self.height  # convert python values into c++ integers
            self.img_array = self.img_array()

        else :
            raise print("Invalid format. Check the IMGFRMT_LIST in camera_config")

    def get_img(self):
        # Capture style
        # IS_DONT_WAIT mode : c_int(0)
        # self.uEyeDll.is_CaptureVideo(self.CAM, c_int(0))
        self.uEyeDll.is_FreezeVideo(self.CAM, c_int(1))
        self.uEyeDll.is_CopyImageMem(self.CAM, self.pcImgMem, self.pid, self.img_array)


        img_array = np.frombuffer(self.img_array, dtype=ctypes.c_ubyte)
        image = np.reshape(img_array, (self.height, self.width, self.channel)).astype('uint8')

        # BGR -> RGB TEST IMAGE SHOW
        b, g, r, a = image.T
        k = np.array([r, g, b, a])
        image = k.transpose()
        test = Image.fromarray(image, mode='RGBA')
        test.show()
