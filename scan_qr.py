import time
import RPi.GPIO as GPIO
import cv2

relay = 19   #khoa dien
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)
GPIO.output(relay, GPIO.LOW)
sec = 0
time_close = 10
def open_box():
    sec = time.time()
    while True:
        GPIO.output(relay, GPIO.HIGH)
        if time.time() - sec >= time_close:
            GPIO.output(relay, GPIO.LOW)
            break
    GPIO.cleanup()