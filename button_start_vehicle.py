from time import sleep
import RPi.GPIO as GPIO
import cv2
import requests
from common import *
button = 4
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN)
pressButton = 1
def start_button():
    status = 0
    pressButton = 1
    while True:
        print(pressButton)
        pressButton = GPIO.input(button)
        if pressButton == 0:
            print("Calling")
            response = requests.get(API_ENDPOINT + URI_START_DELIVERY+"?vehicle_code=" + CODE)
            print(response.status_code)
            status = response.status_code
        if status == 200:
            status = 0
            return 0
    GPIO.cleanup()