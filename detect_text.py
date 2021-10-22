import cv2
import pytesseract
from picamera.array import PiRGBArray
from picamera import PiCamera
import datetime
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(640, 480))

for frame in camera.capture_continuous(rawCapture,format='bgr', use_video_port=True):
    image = frame.array
    cv2.imshow('frame',image)
    key = cv2.waitKey(1) & 0xff
    now = datetime.datetime.now()
    rawCapture.truncate(0)

    text = pytesseract.image_to_string(image)
    print(now)
#     print("ra r: ",text)
    if "SY" in text:
        print("day R")
    cv2.imshow('frame',image)