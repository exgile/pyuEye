import ctypes

# ERROR CODES
IS_NO_SUCCESS                =  -1
IS_SUCCESS                   =   0
IS_INVALID_CAMERA_HANDLE     =   1
IS_INVALID_HANDLE            =   1
IS_IO_REQUEST_FAILED         =   2
IS_CANT_OPEN_DEVICE          =   3

# COLOR MODE CODES
IS_CM_BGRA8_PACKED           =  ctypes.c_int(0)   # BGRA (8, 8, 8, 8), occupies 32 bits.
IS_CM_BGR8_PACKED            =  ctypes.c_int(1)   # BGR (8, 8, 8), occupies 24 bits.
IS_CM_BGR565_PACKED          =  ctypes.c_int(2)   # BGR (5, 6, 5), occupies 16 bits.
IS_CM_BGR5_PACKED            =  ctypes.c_int(3)   # BGR (5, 5, 5, 1), 1 bit not used, occupies 16 bits
IS_CM_MONO8                  =  ctypes.c_int(6)   # GRAY, occupies 8 bits
IS_CM_SENSOR_RAW8            =  ctypes.c_int(11)  # gray, occupies 8 bits
IS_CM_CBYCRY_PACKED          =  ctypes.c_int(23)  # YCbCr422 (8 8), occupies 16 bits

# IMAGE FORMAT CODES
IMGFRMT_CMD_SET_FORMAT       =  ctypes.c_int(3)

# IMAGE FORMAT LIST
# structure : ("  Resolution" :  format ID, width, height  )
IMGFRMT = { "2592x1944" : (ctypes.c_int(4), 2592, 1944),
            "2048x1536" : (ctypes.c_int(5), 2592, 1944),
            "1920x1080" : (ctypes.c_int(6), 1920, 1080),
            "1280x960" : (ctypes.c_int(8), 1280, 960),
            "1280x720" : (ctypes.c_int(9), 1280, 720),
            "800x480" : (ctypes.c_int(12), 800, 480),
            "640x480" : (ctypes.c_int(31), 640, 480),
            "1600x1200" : (ctypes.c_int(20), 1600, 1200)
            # "640x480HS" : ctypes.c_int(31)
          }
