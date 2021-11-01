from time import sleep
import RPi.GPIO as GPIO
import cv2
import requests
from common import *
relay = 19
button = 4
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)
GPIO.setup(button, GPIO.IN)
GPIO.output(relay, GPIO.LOW)
pressButton = 1
def start_button():
    status = 0
    while True:
        pressButton = GPIO.input(button)
        if pressButton == 0:
            print("Calling")
            response = requests.get(API_ENDPOINT + URI_START_DELIVERY+"?vehicle_code=" + CODE)
            print(response.status_code)
            status = response.status_code
        GPIO.output(relay, GPIO.LOW)
        if status == 200:
            return 0
        
    GPIO.cleanup()