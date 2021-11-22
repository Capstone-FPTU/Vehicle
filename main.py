#!/usr/bin/python
import cv2
import RPi.GPIO as GPIO
import pytesseract
import concurrent.futures as cf
import threading
import time
import argparse
import requests
import getmac
import datetime
import multiprocessing
from gpiozero import DistanceSensor
from imutils.perspective import four_point_transform
from common import *

# from play_music import music
enRight = 12
enLeft = 13

inRight1 = 17
inRight2 = 27

inLeft1 = 23
inLeft2 = 22

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

dis = 20
# roley
relay = 3
relayLed = 5
button = 4
GPIO.setup(relay, GPIO.OUT)
GPIO.setup(relayLed, GPIO.OUT)
GPIO.setup(button, GPIO.IN)
GPIO.output(relay, GPIO.LOW)
GPIO.output(relayLed, GPIO.LOW)
frequency = 1000
speed = 100
speedTurn = 80
runLeft = GPIO.PWM(enLeft, frequency)
runRight = GPIO.PWM(enRight, frequency)
runLeft.start(speed)
runRight.start(speed)
cap = cv2.VideoCapture(0)

# detect traffic sign
flag_prioritize = 0
detect = None
sensor = DistanceSensor(echo=25, trigger=24, max_distance=5)
net = ''
flag_sensor_light = "C"
flag_detect = 0
value_detect = ''
villa_name = ''
value = ''
flag_derection_return_home = ""
sign_1 = 0
sign_2 = 0
sign_3 = 0
sign_4 = 0
sign_5 = 0
value_person = 0
flag_turn_sos_p = 0
flag_skip = 0
sec = 0
sec_person = 0
flag_count_parking = 0
flag_turn_parking = 0
sec_call_api = 0
time_call_api = 30
string_api = ''

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
    runLeft.ChangeDutyCycle(speedTurn)
    runRight.ChangeDutyCycle(speedTurn)
    GPIO.output(inRight1, GPIO.HIGH)
    GPIO.output(inRight2, GPIO.LOW)
    GPIO.output(inLeft1, GPIO.LOW)
    GPIO.output(inLeft2, GPIO.HIGH)


def turn_right_max_sos():
    runLeft.ChangeDutyCycle(speedTurn)
    runRight.ChangeDutyCycle(speedTurn)
    GPIO.output(inRight1, GPIO.LOW)
    GPIO.output(inRight2, GPIO.HIGH)
    GPIO.output(inLeft1, GPIO.HIGH)
    GPIO.output(inLeft2, GPIO.LOW)

def turn_left_max_parking():
    runLeft.ChangeDutyCycle(speedTurn + 5)
    runRight.ChangeDutyCycle(speedTurn)
    GPIO.output(inRight1, GPIO.HIGH)
    GPIO.output(inRight2, GPIO.LOW)
    GPIO.output(inLeft1, GPIO.LOW)
    GPIO.output(inLeft2, GPIO.HIGH)


def turn_right_max_parking():
    runLeft.ChangeDutyCycle(speedTurn)
    runRight.ChangeDutyCycle(speedTurn + 5)
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
    if sign_1 == 1 and sign_2 == 1 and sign_3 == 0 and sign_4 == 1 and sign_5 == 1:
        flag_sensor_light = "C"
    elif sign_1 == 0 and sign_2 == 0 and sign_3 == 0 and sign_4 == 0 and sign_5 == 0:
        flag_sensor_light = "SOS_P"
    elif sign_1 == 1 and sign_2 == 0 and sign_4 == 1 and sign_5 == 1:
        flag_sensor_light = "L"
    elif sign_1 == 0 and sign_3 == 1 and sign_4 == 1 and sign_5 == 1:
        flag_sensor_light = "LM"
    elif sign_1 == 1 and sign_2 == 1 and sign_4 == 0 and sign_5 == 1:
        flag_sensor_light = "R"
    elif sign_1 == 1 and sign_2 == 1 and sign_3 == 1 and sign_5 == 0:
        flag_sensor_light = "RM"
    elif sign_1 == 0 and sign_2 == 0 and sign_3 == 0 and sign_5 == 1:
        flag_sensor_light = "SOS_L"
    elif sign_1 == 1 and sign_3 == 0 and sign_4 == 0 and sign_5 == 0:
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
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        morphological_img = cv2.morphologyEx(frame, cv2.MORPH_GRADIENT, kernel)
        canny_img = cv2.Canny(morphological_img, 200, 300)
        contours, _ = cv2.findContours(canny_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        for contour in contours:
            area = cv2.contourArea(contour)
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.015 * peri, True)
            if len(approx) == 4 and area > 4000:
                x, y, w, h = cv2.boundingRect(approx)
                if w > h:
                    ROI = four_point_transform(frame, approx.reshape(4, 2))
                    # resize image
                    scale_percent = 220  # percent of original size
                    width = int(ROI.shape[1] * scale_percent / 100)
                    height = int(ROI.shape[0] * scale_percent / 100)
                    dim = (width, height)
                    resized = cv2.resize(ROI, dim, interpolation=cv2.INTER_AREA)
                    cv2.imwrite("ROI.png", resized)
                    custom_config = r'c tessedit_char_whitelist=HOMELUXTEPYNAIS --psm 6'
                    villa_name = pytesseract.image_to_string(resized, config=custom_config, lang='eng')
                    print("villa:", villa_name)
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


def detect_person(frame):
    global value_person, net
    # detect person
    parser = argparse.ArgumentParser(description='Use MobileNet SSD on Pi for object detection')
    parser.add_argument("--prototxt", default="MobileNetSSD_deploy.prototxt")
    parser.add_argument("--weights", default="MobileNetSSD_deploy.caffemodel")
    argsPer = parser.parse_args()

    net = cv2.dnn.readNetFromCaffe(argsPer.prototxt, argsPer.weights)
    # Resize anh ve 300x300
    frame_resized = cv2.resize(frame, (300, 300))

    # Doc blob va dua vao mang predict
    blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
    net.setInput(blob)
    detections = net.forward()

    # Xu ly output cua mang
    cols = frame_resized.shape[1]
    rows = frame_resized.shape[0]

    # Duyet qua cac object detect duoc
    for i in range(detections.shape[2]):
        # Lay gia tri confidence
        confidence = detections[0, 0, i, 2]
        # Neu vuot qua 0.5 threshold
        if confidence > 0.8:
            class_id = int(detections[0, 0, i, 1])
            if (class_id == 15):
                value_person = confidence
                return
    value_person = 0


def call_thread_detect_person(frame):
    x = threading.Thread(target=detect_person, args=(frame,))
    x.start()
    x.join()

# Vehicle_1 go Parking_Left
def turn_into_home(turn, code):
    global flag_count_parking, flag_call_api
    if flag_count_parking == 0:
        flag_turn_parking = 0
        while True:
            frame = call_thread_camera()
            forward_with_speed(speed)
            call_thread_led_sign()
            if turn == "RIGHT":
                turn_right_max_parking()
                if sign_1 == 0:
                    flag_turn_parking = 1
            else:
                turn_left_max_parking()
                if sign_5 == 0:
                    flag_turn_parking = 1
            if sign_1 == 1 and sign_2 == 1 and sign_3 == 0 and sign_4 == 1 and sign_5 == 1 and flag_turn_parking == 1:
                break
    elif flag_count_parking == 1:
        flag_turn_parking = 0
        while True:
            frame = call_thread_camera()
            forward_with_speed(speed)
            call_thread_led_sign()
            if (code == 'VH001'):
                turn_left_max_parking()
                if sign_5 == 0:
                    flag_turn_parking = 1
            if (code == 'VH002'):
                turn_right_max_parking()
                if sign_1 == 0:
                    flag_turn_parking = 1
            if sign_1 == 1 and sign_2 == 1 and sign_3 == 0 and sign_4 == 1 and sign_5 == 1 and flag_turn_parking == 1:
                break
    elif flag_count_parking == 2:
        flag_turn_parking = 0
        while True:
            frame = call_thread_camera()
            forward_with_speed(speed)
            turn_right_max_sos()
            call_thread_led_sign()
            if sign_5 == 0:
                flag_turn_parking = 1
            if sign_1 == 1 and sign_2 == 1 and sign_3 == 0 and sign_4 == 1 and sign_5 == 1 and flag_turn_parking == 1:
                stop()
                api = API_ENDPOINT + URI_FINISH + "?vehicle_code=" + code
                requests.get(api)
                break


def go_out_parking(turn):
    flag_turn_parking = 0
    while True:
        frame = call_thread_camera()
        forward_with_speed(speed)
        call_thread_led_sign()
        if turn == "RIGHT":
            turn_right_max_sos()
            if sign_1 == 0:
                flag_turn_parking = 1
        elif turn == "LEFT":
            turn_left_max_sos()
            if sign_5 == 0:
                flag_turn_parking = 1
        if sign_1 == 1 and sign_2 == 1 and sign_3 == 0 and sign_4 == 1 and sign_5 == 1 and flag_turn_parking == 1:
            break


def reset():
    global flag_prioritize, detect, flag_sensor_light, flag_detect, value_detect, villa_name, value, flag_derection_return_home, flag_call_api
    global sign_1, sign_2, sign_3, sign_4, sign_5, value_person, flag_turn_sos_p, flag_skip, sec, sec_person, flag_count_parking, flag_turn_parking
    flag_prioritize = 0
    detect = None
    flag_sensor_light = "C"
    flag_detect = 0
    value_detect = ''
    villa_name = ''
    value = ''
    flag_derection_return_home = ""
    sign_1 = 0
    sign_2 = 0
    sign_3 = 0
    sign_4 = 0
    sign_5 = 0
    value_person = 0
    flag_turn_sos_p = 0
    flag_skip = 0
    sec = 0
    sec_person = 0
    flag_count_parking = 0
    flag_turn_parking = 0
    GPIO.output(relayLed, GPIO.LOW)
    flag_call_api = False


def turn_180():
    flag_turn_parking = 0
    while True:
        frame = call_thread_camera()
        forward_with_speed(speed)
        turn_right_max_sos()
        call_thread_led_sign()
        if sign_1 == 0 and sign_2 == 1:
            flag_turn_parking = 1
        if sign_1 == 1 and sign_2 == 1 and sign_3 == 0 and sign_4 == 1 and sign_5 == 1 and flag_turn_parking == 1:
            break

def upload_image_sos(code):
    files = {'files': open('image.jpg', 'rb')}
    api = API_ENDPOINT + URI_SOS + "?vehicle_code=" + code + "&mac_address=" + getmac.get_mac_address()
    x = requests.post(api, files=files)
    print(x.status_code)

def call_api(data):
    x = requests.get(data)
    print(x.status_code)
    
def call_api_process(data):
    p1 = multiprocessing.Process(target=call_api, args=(data,))
    p1.start()
    
def run(list_villa, home_value, code, isTurning, value_turning, fullWay):
    global value_detect, villa_name, value_person, flag_skip, sec, flag_sensor_light, sec_call_api
    global flag_derection_return_home, flag_turn_sos_p, flag_count_parking, flag_turn_parking, flag_call_api
    convert_list = list(list_villa)
    flag_go_out = 0
    if home_value == '':
        flag_go_out = 1

    if value_turning:
        if value_turning == "FORWARD":
            value_turning = ''
        value_detect = value_turning
        value_turning = ''
    while True:
        flag_detect = 0
        frame = call_thread_camera()
        cv2.imwrite("image.jpg", frame)
        key = cv2.waitKey(1)
        if isTurning:
            turn_180()
            isTurning = False

        if value_detect == "STOP":
            stop()
            reset()
            value_detect = ''
            flag_go_out = 0
            flag_skip = 0
            api = API_ENDPOINT + URI_ARRIVED + "?vehicle_code=" + code
            requests.get(api)
#             music("hello.wav")
            list_villa= ''
            return 0
        # detect distance
        while sensor.distance * 100 < dis and value_person == 0:
            if sec_call_api == 0:
                sec_call_api = time.time()
            if time.time() - sec_call_api >= time_call_api:
                print("sos call api detect")
                upload_image_sos(code)
                reset()
                return 0
            stop()
            call_thread_detect_person(frame)
            if value_person > 0:
                print("Person")
                value_person = 0
            else:
                print("Obstacle")
                call_thread_led_sign()
                call_thread_follow_line(sign_1, sign_2, sign_3, sign_4, sign_5)

        call_thread_led_sign()
        call_thread_follow_line(sign_1, sign_2, sign_3, sign_4, sign_5)
        GPIO.output(relayLed, GPIO.LOW)
        
        if flag_sensor_light == "SOS_P" and flag_derection_return_home != "":
            flag_count_parking = flag_count_parking + 1
            turn_into_home(flag_derection_return_home, code)
            if flag_count_parking == 2:
                stop()
                reset()
                flag_sensor_light = ''
                flag_derection_return_home = ''
                flag_count_parking = 0
                return 0
        if flag_sensor_light == "SOS_P":
            if value_detect == "":
                GPIO.output(relayLed, GPIO.HIGH)
                flag_turn_sos_p = 0
                stop()
                if sec_call_api == 0:
                    sec_call_api = time.time()
                frame = call_thread_camera()
                call_thread_detect_villa(frame)
                if villa_name == "" and time.time() - sec_call_api >= time_call_api:
                    print("sos call api")
                    upload_image_sos(code)
                    reset()
                    return 0
                if villa_name != "":
                    villa = "".join(filter(str.isalnum, villa_name))
                try:
                    value_detect = list_villa[villa].upper().strip()
                    GPIO.output(relayLed, GPIO.LOW)
                    api = API_ENDPOINT + URI_TRACKING + "?vehicle_code=" + code + "&villa_name=" + villa + "&way=" + fullWay + "&before_node=" + convert_list[convert_list.index(villa) - 1]
                    call_api_process(api)
#                     requests.get(api)
                    # end call
                    flag_call_api = False
                    villa_name = ''
                    villa = ''
                    flag_detect = 1
                    flag_skip = 1
                    sec = time.time()
                    forward_with_speed(speed)
                    sec_call_api = 0
                    call_thread_follow_line(sign_1, sign_2, sign_3, sign_4, sign_5)
                except:
                    value_detect = value_detect
                    # GPIO.output(relayLed, GPIO.LOW)
            #         nga tu
            elif value_detect != "" and flag_skip == 1 and time.time() - sec > 1:
                print('---------------------------------------')
                sec = time.time()
                flag_skip = 0
                forward_with_speed(speed)
                call_thread_follow_line(sign_1, sign_2, sign_3, sign_4, sign_5)
            elif value_detect != "" and flag_skip == 0 and time.time() - sec > 1:
                forward_with_speed(speed)
                call_thread_follow_line(sign_1, sign_2, sign_3, sign_4, sign_5)
                flag_turn_parking = 0
                if flag_turn_sos_p == 1:
                    if value_detect == "FORWARD":
                        forward_with_speed(speed)
                        value_detect = ''
                        flag_turn_sos_p = 0
                    while value_detect == "LEFT" and flag_detect == 0 and time.time() - sec > 1:
                        frame = call_thread_camera()
                        turn_left_max_sos()
                        call_thread_led_sign()
                        if sign_2 == 0 and sign_1 == 1:
                            flag_turn_parking = 1
                        if sign_1 == 1 and sign_2 == 1 and sign_3 == 0 and sign_4 == 1 and sign_5 == 1 and flag_turn_parking == 1:
                            value_detect = ''
                            break
                    while value_detect == "RIGHT" and flag_detect == 0 and time.time() - sec > 1:
                        frame = call_thread_camera()
                        turn_right_max_sos()
                        call_thread_led_sign()
                        if sign_4 == 0 and sign_5 == 1:
                            flag_turn_parking = 1
                        if sign_1 == 1 and sign_2 == 1 and sign_3 == 0 and sign_4 == 1 and sign_5 == 1 and flag_turn_parking == 1:
                            value_detect = ''
                            break


        #     nga ba
        else:
            sec_call_api = 0
            flag_turn_sos_p = 1
            forward_with_speed(speed)
            call_thread_follow_line(sign_1, sign_2, sign_3, sign_4, sign_5)
            # nga ba

            if flag_sensor_light == "SOS_L":
                if flag_go_out == 0:
                    go_out_parking("LEFT")
                    value_detect = home_value
                    flag_go_out = 1
                else:
                    flag_turn_parking = 0
                    if flag_skip == 1 and time.time() - sec > 1:
                        sec = time.time()
                        flag_skip = 0
                    if value_detect == "PARKING" and flag_derection_return_home == "" and flag_skip == 0 and time.time() - sec > 1:
                        flag_derection_return_home = "LEFT"
                        turn_into_home(flag_derection_return_home, code)
                    if value_detect == "FORWARD" and time.time() - sec > 1:
                        forward_with_speed(speed)
                        value_detect = ''
                        flag_turn_sos_p = 0
                    while value_detect == "LEFT" and flag_detect == 0 and flag_skip == 0 and time.time() - sec > 0.5:
                        frame = call_thread_camera()
                        turn_left_max_sos()
                        call_thread_led_sign()
                        if sign_5 == 0:
                            flag_turn_parking = 1
                        if sign_1 == 1 and sign_2 == 1 and sign_3 == 0 and sign_4 == 1 and sign_5 == 1 and flag_turn_parking == 1:
                            value_detect = ''
                            break
            elif flag_sensor_light == "SOS_R":
                if flag_go_out == 0:
                    go_out_parking("RIGHT")
                    value_detect = home_value
                    flag_go_out = 1
                else:
                    flag_turn_parking = 0
                    if flag_skip == 1 and time.time() - sec > 1:
                        sec = time.time()
                        flag_skip = 0
                    if value_detect == "PARKING" and flag_derection_return_home == "" and flag_skip == 0 and time.time() - sec > 1:
                        flag_derection_return_home = "RIGHT"
                        turn_into_home(flag_derection_return_home, code)
                    if value_detect == "FORWARD" and time.time() - sec > 1:
                        forward_with_speed(speed)
                        value_detect = ''
                        flag_turn_sos_p = 0
                    while value_detect == "RIGHT" and flag_detect == 0 and flag_skip == 0 and time.time() - sec > 0.5:
                        frame = call_thread_camera()
                        turn_right_max_sos()
                        call_thread_led_sign()
                        if sign_1 == 0:
                            flag_turn_parking = 1
                        if sign_1 == 1 and sign_2 == 1 and sign_3 == 0 and sign_4 == 1 and sign_5 == 1 and flag_turn_parking == 1:
                            value_detect = ''
                            break
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
        if (key == ord('q')):
            GPIO.output(relayLed, GPIO.LOW)
            break

    GPIO.output(inRight1, GPIO.LOW)
    GPIO.output(inRight2, GPIO.LOW)
    GPIO.output(inLeft1, GPIO.LOW)
    GPIO.output(inLeft2, GPIO.LOW)
    cap.release()
    cv2.destroyAllWindows()
