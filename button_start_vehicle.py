from time import sleep
import RPi.GPIO as GPIO
import cv2
import requests
from common import *
button = 4

pressButton = 1
def start_button():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button, GPIO.IN)
    sleep(0.5)
    status = 0
    pressButton = 1
    while True:
        pressButton = GPIO.input(button)
        print(pressButton)
        if pressButton == 0:
            print("Calling")
            response = requests.get(API_ENDPOINT + URI_START_DELIVERY+"?vehicle_code=" + CODE)
            print(response.status_code)
            status = response.status_code
        if status == 200:
            status = 0
            return 0
    GPIO.cleanup()