import cv2
import RPi.GPIO as GPIO          
from time import sleep
from gpiozero import DistanceSensor
import datetime
import pytesseract
import numpy as np
import concurrent.futures as cf

enRight = 12
enLeft = 13

inRight1 = 17
inRight2 = 27

inLeft1 = 23
inLeft2 =  22

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

GPIO.setup(enRight, GPIO.OUT)
GPIO.setup(enLeft, GPIO.OUT)

GPIO.setup(inRight1, GPIO.OUT)
GPIO.setup(inRight2, GPIO.OUT)

GPIO.setup(inLeft1, GPIO.OUT)
GPIO.setup(inLeft2, GPIO.OUT)

GPIO.output(inRight1, GPIO.LOW)
GPIO.output(inRight2, GPIO.LOW)
GPIO.output(inLeft1, GPIO.LOW)
GPIO.output(inLeft2, GPIO.LOW)

frequency = 1000
speed = 100
runLeft = GPIO.PWM(enLeft, frequency)
runRight = GPIO.PWM(enRight, frequency)
runLeft.start(speed)
runRight.start(speed)
cap = cv2.VideoCapture(0)

# detect traffic sign
detect_right = cv2.CascadeClassifier('data_traffic_signs/right.xml')
detect_left = cv2.CascadeClassifier('data_traffic_signs/left.xml')
detect_stop = cv2.CascadeClassifier('data_traffic_signs/stop_new.xml')
flag_prioritize = 0
detect = None
sensor = DistanceSensor(echo=18, trigger=24, max_distance=5)

def detect_villa(frame):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5, 5))
    morphological_img = cv2.morphologyEx(frame, cv2.MORPH_GRADIENT, kernel)
    canny_img = cv2.Canny(morphological_img, 200, 300)
    contours, _ = cv2.findContours(
        canny_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.015 * peri, True)
        if len(approx) == 4 and area > 3000:
            x, y, w, h = cv2.boundingRect(approx)
            if w > h:
                ROI = frame[y:y + h, x:x + w]
                custom_config = r'c tessedit_char_whitelist=HOMELUXTEPYNAIS --psm 6'
                text = pytesseract.image_to_string(ROI, config=custom_config)
                if text is not None:
                    return text
                

def detect_traffic_sign(gray):
    for k, v in array.items():
        detect = v.detectMultiScale(gray, 1.9, 7)
        if type(detect) != tuple:
            return k
            
def forward_with_speed(speed):
    runLeft.ChangeDutyCycle(speed)
    runRight.ChangeDutyCycle(speed)
    GPIO.output(inRight1, GPIO.LOW)
    GPIO.output(inRight2, GPIO.HIGH)
    GPIO.output(inLeft1, GPIO.LOW)
    GPIO.output(inLeft2, GPIO.HIGH)
def turn_right(turn_value):
    runLeft.ChangeDutyCycle(turn_value)
    GPIO.output(inRight1, GPIO.LOW)
    GPIO.output(inRight2, GPIO.HIGH)
    GPIO.output(inLeft1, GPIO.LOW)
    GPIO.output(inLeft2, GPIO.LOW)
def turn_left(turn_value):
#     runLeft.ChangeDutyCycle(100)
    runRight.ChangeDutyCycle(turn_value)
    GPIO.output(inRight1, GPIO.LOW)
    GPIO.output(inRight2, GPIO.LOW)
    GPIO.output(inLeft1, GPIO.LOW)
    GPIO.output(inLeft2, GPIO.HIGH)
def turn_right_max():
    GPIO.output(inRight1, GPIO.LOW)
    GPIO.output(inRight2, GPIO.HIGH)
    GPIO.output(inLeft1, GPIO.LOW)
    GPIO.output(inLeft2, GPIO.LOW)
def turn_left_max():
    GPIO.output(inRight1, GPIO.LOW)
    GPIO.output(inRight2, GPIO.LOW)
    GPIO.output(inLeft1, GPIO.LOW)
    GPIO.output(inLeft2, GPIO.HIGH)
def turn_left_max_sos():
    runLeft.ChangeDutyCycle(70)
    runRight.ChangeDutyCycle(70)
    GPIO.output(inRight1, GPIO.HIGH)
    GPIO.output(inRight2, GPIO.LOW)
    GPIO.output(inLeft1, GPIO.LOW)
    GPIO.output(inLeft2, GPIO.HIGH)
def turn_right_max_sos():
    runLeft.ChangeDutyCycle(70)
    runRight.ChangeDutyCycle(70)
    GPIO.output(inRight1, GPIO.LOW)
    GPIO.output(inRight2, GPIO.HIGH)
    GPIO.output(inLeft1, GPIO.HIGH)
    GPIO.output(inLeft2, GPIO.LOW)
def stop():
    GPIO.output(inRight1, GPIO.LOW)
    GPIO.output(inRight2, GPIO.LOW)
    GPIO.output(inLeft1, GPIO.LOW)
    GPIO.output(inLeft2, GPIO.LOW)

flag_sensor_light = "C"
flag_detect_traffic_sign = 0
value_traffic_sign = ''
def follow_line(sign_1, sign_2, sign_3, sign_4, sign_5):
    global flag_sensor_light
    if sign_1 == 1 and  sign_2 == 1  and sign_3 == 0 and sign_4 == 1 and sign_5 == 1:
        flag_sensor_light = "C"
    elif sign_1 == 1 and sign_2 == 0 and sign_4 == 1 and sign_5 == 1:
        flag_sensor_light = "L"
    elif  sign_1 == 0 and sign_3 == 1 and sign_4 == 1 and sign_5 == 1:
        flag_sensor_light = "LM"
    elif sign_1 == 1 and sign_2 == 1 and sign_4 == 0 and sign_5 == 1:
        flag_sensor_light = "R"
    elif sign_1 == 1 and sign_2 == 1 and sign_3 == 1 and sign_5 == 0:
        flag_sensor_light = "RM"
    elif sign_1 == 0 and sign_2 == 0 and sign_3 == 0 :
        flag_sensor_light = "SOS"
    elif sign_3 == 0 and sign_4 == 0 and sign_5 == 0:
        flag_sensor_light = "SOS"

def open_cam():
    ret, frame = cap.read()
    return frame

list_villa = {
    "Home": "stop",
    "Sona": "right",
    "Yuumi": "right",
    "Aster": "right",
}

array = {
    'STOP': detect_stop,
    'RIGHT': detect_right,
    'LEFT': detect_left
    }
while True:
#     print(flag_sensor_light)
    frame = ''
    with cf.ThreadPoolExecutor() as executor:
        future = executor.submit(open_cam)
        frame = future.result()
    key = cv2.waitKey(1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("New Vehicle", frame)
    
    # detect distance
    while sensor.distance * 100 < 20:
        print("DUng lai")
        stop()
    
    # end detect distance
    forward_with_speed(speed)
    sign_1 = GPIO.input(sensor_1)
    sign_2 = GPIO.input(sensor_2)
    sign_3 = GPIO.input(sensor_3)
    sign_4 = GPIO.input(sensor_4)
    sign_5 = GPIO.input(sensor_5)
    follow_line(sign_1, sign_2, sign_3, sign_4, sign_5)
#     print(flag_sensor_light)
    if flag_sensor_light == "C":
        forward_with_speed(speed)
    elif flag_sensor_light == "R":
        turn_right(10)
    elif flag_sensor_light == "RM":
        turn_right_max()
    elif flag_sensor_light == "L":
        turn_left(10)
    elif flag_sensor_light == "LM":
        turn_left_max()
    elif flag_sensor_light == "SOS":
        while value_traffic_sign == "LEFT":
            turn_left_max_sos()
            sign_1 = GPIO.input(sensor_1)
            sign_2 = GPIO.input(sensor_2)
            sign_3 = GPIO.input(sensor_3)
            sign_4 = GPIO.input(sensor_4)
            sign_5 = GPIO.input(sensor_5)
            if sign_1 == 0 and sign_2 == 0 and sign_3 == 1 and sign_4 == 1 and sign_5 == 1:
                # return init value
                flag_detect_traffic_sign = 0
                value_traffic_sign = ''
        while value_traffic_sign == "RIGHT":
            with cf.ThreadPoolExecutor() as executor:
                future = executor.submit(open_cam)
                frame = future.result()
            turn_right_max_sos()
            sign_1 = GPIO.input(sensor_1)
            sign_2 = GPIO.input(sensor_2)
            sign_3 = GPIO.input(sensor_3)
            sign_4 = GPIO.input(sensor_4)
            sign_5 = GPIO.input(sensor_5)
            if sign_1 == 1 and sign_2 == 1 and sign_3 == 1 and sign_4 == 0 and sign_5 == 0:
                # return init value
                flag_detect_traffic_sign = 0
                value_traffic_sign = ''
        while value_traffic_sign == "STOP":
            stop()
            # return init value
#             flag_detect_traffic_sign = 0
#             value_traffic_sign = ''
    # de.tect traffic sign
    value = detect_traffic_sign(gray)
    villa_name = detect_villa(frame)
    print(villa_name)
    
    if value is not None:
        flag_detect_traffic_sign = 1
        value_traffic_sign = value
    # detect villa
    if villa_name is not None:
        villa = "".join(filter(str.isalnum, villa_name))
        for key, value in list_villa.items():
            if villa.upper().strip() == key.upper().strip():
                value_traffic_sign = value.upper().strip()
    # end detect villa    
    print(value_traffic_sign)
    # end detect t_s
    if(key==ord('q')):
        break
    if(key==ord('w')):
        forward_with_speed(50)
    if(key==ord('a')):
        turn_left()
    if(key==ord('d')):
        turn_right()
    
GPIO.output(inRight1, GPIO.LOW)
GPIO.output(inRight2, GPIO.LOW)
GPIO.output(inLeft1, GPIO.LOW)
GPIO.output(inLeft2, GPIO.LOW)
cap.release()
cv2.destroyAllWindows()


