from time import sleep
import RPi.GPIO as GPIO
import cv2

relay = 5
button = 4
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)
GPIO.setup(button, GPIO.IN)
GPIO.output(relay, GPIO.LOW)
pressButton = 1
while True:
    pressButton = GPIO.input(button)
    print(pressButton)
    if pressButton == 0:
        GPIO.output(relay,GPIO.HIGH)
        sleep(2)
    GPIO.output(relay, GPIO.LOW)
    
GPIO.cleanup()
