#!/usr/bin/python
import cv2
import RPi.GPIO as GPIO
from gpiozero import DistanceSensor
import datetime
import pytesseract
import numpy as np
import concurrent.futures as cf
import threading
import numpy
from imutils.perspective import four_point_transform
import datetime

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
flag_prioritize = 0
detect = None
sensor = DistanceSensor(echo=25, trigger=24, max_distance=5)

flag_sensor_light = "C"
flag_detect = 0
value_detect = ''
villa_name = ''
value = ''
sign_1 = 0
sign_2 = 0
sign_3 = 0
sign_4 = 0
sign_5 = 0

list_villa = {
    "HOME": "left",
    "SONA": "forward",
    "YUMMI": "forward",
    "NAMI": "forward",
    "LULU": "right",
    "LUX": "left",
    "TEEMO": "stop"
}

            
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
    runLeft.ChangeDutyCycle(90)
    runRight.ChangeDutyCycle(90)
    GPIO.output(inRight1, GPIO.HIGH)
    GPIO.output(inRight2, GPIO.LOW)
    GPIO.output(inLeft1, GPIO.LOW)
    GPIO.output(inLeft2, GPIO.HIGH)
def turn_right_max_sos():
    runLeft.ChangeDutyCycle(90)
    runRight.ChangeDutyCycle(90)
    GPIO.output(inRight1, GPIO.LOW)
    GPIO.output(inRight2, GPIO.HIGH)
    GPIO.output(inLeft1, GPIO.HIGH)
    GPIO.output(inLeft2, GPIO.LOW)
def stop():
    GPIO.output(inRight1, GPIO.LOW)
    GPIO.output(inRight2, GPIO.LOW)
    GPIO.output(inLeft1, GPIO.LOW)
    GPIO.output(inLeft2, GPIO.LOW)


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
    elif sign_1 == 1 and sign_3 == 0 and sign_4 == 0 and sign_5 == 0 :
        flag_sensor_light = "SOS_R"

def call_thread_follow_line(sign_1, sign_2, sign_3, sign_4, sign_5):
    x = threading.Thread(target=follow_line, args=(sign_1, sign_2, sign_3, sign_4, sign_5))
    x.start()
    x.join()

def open_camera():
    ret, frame = cap.read()
    return frame

def call_thread_camera():
    with cf.ThreadPoolExecutor() as executor:
        future = executor.submit(open_camera)
        frame = future.result()
        return frame

def detect_villa(frame):
    global villa_name
    global flag_detect
    
    
    if flag_detect == 0:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5, 5))
        morphological_img = cv2.morphologyEx(frame, cv2.MORPH_GRADIENT, kernel)
        canny_img = cv2.Canny(morphological_img, 200, 300)
        contours, _ = cv2.findContours(canny_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        coutours = sorted(contours, key=cv2.contourArea, reverse=True)
        for contour in contours:
            area = cv2.contourArea(contour)
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.015 * peri, True)
            if len(approx) == 4 and area > 5000:
                x, y, w, h = cv2.boundingRect(approx)
                if w > h:
                    ROI = four_point_transform(frame, approx.reshape(4, 2))
                    # resize image
                    scale_percent = 220 # percent of original size
                    width = int(ROI.shape[1] * scale_percent / 100)
                    height = int(ROI.shape[0] * scale_percent / 100)
                    dim = (width, height)
                    resized = cv2.resize(ROI, dim, interpolation = cv2.INTER_AREA)                    
                    
                    
                    cv2.imwrite("ROI.png",resized)
                    custom_config = r'c tessedit_char_whitelist=HOMELUXTEPYNAIS --psm 6'
                    villa_name = pytesseract.image_to_string(resized, config=custom_config, lang='eng')
                    print(villa_name)
                    if villa_name != "":
                        break
                    
    else:
        villa_name = ''

def call_thread_detect_villa(frame):
    x = threading.Thread(target=detect_villa, args=(frame,))
    x.start()
    x.join()
    


def led_sign():
    global sign_1, sign_2, sign_3, sign_4, sign_5 
    sign_1 = GPIO.input(sensor_1)
    sign_2 = GPIO.input(sensor_2)
    sign_3 = GPIO.input(sensor_3)
    sign_4 = GPIO.input(sensor_4)
    sign_5 = GPIO.input(sensor_5)
    
def call_thread_led_sign():
    x = threading.Thread(target=led_sign, args=())
    x.start()
    x.join()
    #Vehicle_2 go Parking_Right
def turn_into_home(turn):
    global flag_count_parking
    if flag_count_parking == 0:
        flag_turn_parking = 0
        while True:
            frame = call_thread_camera()
            forward_with_speed(speed)
            call_thread_led_sign()
            if turn == "RIGHT":
                turn_right_max_sos()
                if sign_4 == 0 and sign_5 ==1:
                    flag_turn_parking = 1
            else:
                turn_left_max_sos()
                if sign_2 == 0 and sign_1 ==1:
                    flag_turn_parking =1
            if sign_1 == 1 and sign_2 == 1 and sign_3 == 0 and sign_4 == 1 and sign_5 == 1 and flag_turn_parking ==1:
                break
    elif flag_count_parking == 1:
        flag_turn_parking = 0
        while True:
            frame = call_thread_camera()
            forward_with_speed(speed)
            turn_right_max_sos()
            call_thread_led_sign()
            if sign_4 == 0 and sign_5 ==1:
                    flag_turn_parking =1
            if sign_1 == 1 and sign_2 == 1 and sign_3 == 0 and sign_4 == 1 and sign_5 == 1 and flag_turn_parking ==1:
                break
    elif flag_count_parking == 2:
        flag_turn_parking = 0
        while True:
            frame = call_thread_camera()
            forward_with_speed(speed)
            turn_right_max_sos()
            call_thread_led_sign()
            if sign_2 == 0 and sign_1 == 1:
                flag_turn_parking =1
            if sign_1 == 1 and sign_2 == 1 and sign_3 == 0 and sign_4 == 1 and sign_5 == 1 and flag_turn_parking ==1:
                break
    #Vehicle_1 go Parking_Left
# def turn_into_home(turn):
#     global flag_count_parking
#     if flag_count_parking == 0:
#         flag_turn_parking= 0
#         while True:
#             frame = call_thread_camera()
#             forward_with_speed(speed)
#             call_thread_led_sign()
#             if turn == "RIGHT":
#                 turn_right_max_sos()
#                 if sign_4 == 0 and sign_5 ==1:
#                     flag_turn_parking =1
#             else:
#                 turn_left_max_sos()
#                 if sign_2 == 0 and sign_1 ==1:
#                     flag_turn_parking =1
#             if sign_1 == 1 and sign_2 == 1 and sign_3 == 0 and sign_4 == 1 and sign_5 == 1 and flag_turn_parking ==1:
#                 break
#     elif flag_count_parking == 1:
#         flag_turn_parking = 0
#         while True:
#             frame = call_thread_camera()
#             forward_with_speed(speed)
#             call_thread_led_sign()
#             turn_left_max_sos()
#             if sign_2 == 0 and sign_1 ==1:
#                 flag_turn_parking =1
#             if sign_1 == 1 and sign_2 == 1 and sign_3 == 0 and sign_4 == 1 and sign_5 == 1 and flag_turn_parking ==1:
#                 break
#     elif flag_count_parking == 2:
#         flag_turn_parking = 0
#         while True:
#             frame = call_thread_camera()
#             forward_with_speed(speed)
#             turn_right_max_sos()
#             call_thread_led_sign()
#             if sign_1 == 0 and sign_2 == 1:
#                 flag_turn_parking =1
#             if sign_1 == 1 and sign_2 == 1 and sign_3 == 0 and sign_4 == 1 and sign_5 == 1 and flag_turn_parking ==1:
#                 break
def go_out_parking(turn):
    flag_turn_parking = 0
    while True:
        frame = call_thread_camera()
        forward_with_speed(speed)
        call_thread_led_sign()
        if turn == "RIGHT":
            turn_right_max_sos()
            if sign_4 == 0 and sign_5 ==1:
                flag_turn_parking =1
        elif turn == "LEFT":
            turn_left_max_sos()
            if sign_2 == 0 and sign_1 ==1:
                flag_turn_parking =1
        if sign_1 == 1 and sign_2 == 1 and sign_3 == 0 and sign_4 == 1 and sign_5 == 1 and flag_turn_parking ==1:
                break


# Can bien nay ne Loc
flag_count_parking = 0
########################
flag_turn_sos_p = 0
flag_skip = 0
second_flag_skip = 0
test_count = 0
flag_derection_return_home = ""
while True:
    flag_detect = 0
    frame = call_thread_camera()
    key = cv2.waitKey(1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("New Vehicle", frame)
    
    # detect distance
    while sensor.distance * 100 < 25:
        print("Dung lai")
        stop() 
    call_thread_led_sign()
    print("flag_skip: ", flag_skip)
    print("count: ", test_count)
    print("second_flag_skip: ", second_flag_skip)
    print("value_detect: ", value_detect)
    print("flag_sensor_light: ", flag_sensor_light)
    # end detect distance
    
    call_thread_follow_line(sign_1, sign_2, sign_3, sign_4, sign_5)
    
    if value_detect == "STOP":
        stop()
        key = ord('q')
    if flag_sensor_light == "SOS_P" and flag_derection_return_home != "":
        #Truyen bien tu HOme vao
#         go_out_parking("LEFT")
        ###### Vao PARKING #######
        flag_count_parking = flag_count_parking + 1
        turn_into_home(flag_derection_return_home)
        if flag_count_parking == 2:
            key = ord('q')
        ##########################
    elif flag_sensor_light == "SOS_P":
        #loc viet
        stop()
         
            
                         
#     nga ba 
    else:
        flag_turn_sos_p = 1
        forward_with_speed(speed)
        if value_detect == "FORWARD":
            forward_with_speed(speed)
            value_detect = ''
            flag_turn_sos_p = 0
            ############ Vao Parking ne LOC#######
        if flag_sensor_light == "SOS_L" and flag_derection_return_home == "":
            flag_derection_return_home = "LEFT"
            turn_into_home(flag_derection_return_home)
        elif flag_sensor_light == "SOS_R"  and flag_derection_return_home == "":
            flag_derection_return_home = "RIGHT"
            turn_into_home(flag_derection_return_home)
            ###########################################
#         if flag_sensor_light == "SOS_L" and flag_derection_return_home == "":
#             flag_derection_return_home = "LEFT"
#             go_out_parking(flag_derection_return_home)
# #             key = ord('q')
#             
#         elif flag_sensor_light == "SOS_R" and flag_derection_return_home == "":
#             flag_derection_return_home = "RIGHT"
#             go_out_parking(flag_derection_return_home)
#             key = ord('q')
        elif flag_sensor_light == "C":
            forward_with_speed(speed)
        elif flag_sensor_light == "R":
            turn_right(10)
        elif flag_sensor_light == "RM":
            turn_right_max()
        elif flag_sensor_light == "L":
            turn_left(10)
        elif flag_sensor_light == "LM":
            turn_left_max()
    if(key==ord('q')):
        break
    
GPIO.output(inRight1, GPIO.LOW)
GPIO.output(inRight2, GPIO.LOW)
GPIO.output(inLeft1, GPIO.LOW)
GPIO.output(inLeft2, GPIO.LOW)
cap.release()
cv2.destroyAllWindows()
