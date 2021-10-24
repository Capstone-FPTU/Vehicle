
import cv2
import RPi.GPIO as GPIO          
from time import sleep


sensor_1 = 16
sensor_2 = 20
sensor_3 = 21
sensor_4 = 6
sensor_5 = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# setup pin on PI 
GPIO.setup(sensor_1, GPIO.IN)
GPIO.setup(sensor_2, GPIO.IN)
GPIO.setup(sensor_3, GPIO.IN)
GPIO.setup(sensor_4, GPIO.IN)
GPIO.setup(sensor_5, GPIO.IN)
flag_sensor_light = "C"

def follow_line(sign_1, sign_2, sign_3, sign_4, sign_5):
    global flag_sensor_light
    if sign_1 == 1 and  sign_2 == 1  and sign_3 == 0 and sign_4 == 1 and sign_5 == 1:
        flag_sensor_light = "C"
    elif sign_1 == 0 and sign_2 == 0 and sign_3 == 0 and sign_4 == 0 and sign_5 == 0:
        flag_sensor_light = "SOS_P"
    elif sign_1 == 1 and sign_2 == 0 and sign_4 == 1 and sign_5 == 1:
        flag_sensor_light = "L"
    elif  sign_1 == 0 and sign_3 == 1 and sign_4 == 1 and sign_5 == 1:
        flag_sensor_light = "LM"
    elif sign_1 == 1 and sign_2 == 1 and sign_4 == 0 and sign_5 == 1:
        flag_sensor_light = "R"
    elif sign_1 == 1 and sign_2 == 1 and sign_3 == 1 and sign_5 == 0:
        flag_sensor_light = "RM"
    elif sign_1 == 0 and sign_2 == 0 and sign_3 == 0 and sign_5 == 1:
        flag_sensor_light = "SOS_L"
    elif sign_3 == 0 and sign_4 == 0 and sign_5 == 0 and sign_1 == 1:
        flag_sensor_light = "SOS_R"

        
while True:
    sign_1 = GPIO.input(sensor_1)
    sign_2 = GPIO.input(sensor_2)
    sign_3 = GPIO.input(sensor_3)
    sign_4 = GPIO.input(sensor_4)
    sign_5 = GPIO.input(sensor_5)
    follow_line(sign_1, sign_2, sign_3, sign_4, sign_5)
    print(sign_1, sign_2, sign_3, sign_4, sign_5)
    print(flag_sensor_light)