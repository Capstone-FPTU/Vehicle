import cv2
import RPi.GPIO as GPIO          
from time import sleep

enRight = 12
enLeft = 13

inRight1 = 17
inRight2 = 27

inLeft1 = 22
inLeft2 =  23

# sensor_1 = 16
# sensor_2 = 20
# sensor_3 = 21
# sensor_4 = 6
# sensor_5 = 26

button = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# setup pin on PI 
# GPIO.setup(sensor_1, GPIO.IN)
# GPIO.setup(sensor_2, GPIO.IN)
# GPIO.setup(sensor_3, GPIO.IN)
# GPIO.setup(sensor_4, GPIO.IN)
# GPIO.setup(sensor_5, GPIO.IN)

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
GPIO.setup(button, GPIO.IN)

frequency = 500
speed = 100
runLeft = GPIO.PWM(enLeft, frequency)
runRight = GPIO.PWM(enRight, frequency)
runLeft.start(speed)
runRight.start(speed)
cap = cv2.VideoCapture(0)
pressButton = 1


def forward_with_speed(speed):
    runLeft.ChangeDutyCycle(speed)
    runRight.ChangeDutyCycle(speed)
    GPIO.output(inRight1, GPIO.LOW)
    GPIO.output(inRight2, GPIO.HIGH)
    GPIO.output(inLeft1, GPIO.LOW)
    GPIO.output(inLeft2, GPIO.HIGH)
def turn_left(turn_value):
#     runRight.ChangeDutyCycle(100)
    runLeft.ChangeDutyCycle(turn_value)
    GPIO.output(inRight1, GPIO.LOW)
    GPIO.output(inRight2, GPIO.HIGH)
    GPIO.output(inLeft1, GPIO.LOW)
    GPIO.output(inLeft2, GPIO.LOW)
def turn_right(turn_value):
#     runLeft.ChangeDutyCycle(100)
    runRight.ChangeDutyCycle(turn_value)
    GPIO.output(inRight1, GPIO.LOW)
    GPIO.output(inRight2, GPIO.LOW)
    GPIO.output(inLeft1, GPIO.LOW)
    GPIO.output(inLeft2, GPIO.HIGH)
def turn_left_max():
    GPIO.output(inRight1, GPIO.LOW)
    GPIO.output(inRight2, GPIO.HIGH)
    GPIO.output(inLeft1, GPIO.LOW)
    GPIO.output(inLeft2, GPIO.LOW)
def turn_right_max():
    GPIO.output(inRight1, GPIO.LOW)
    GPIO.output(inRight2, GPIO.LOW)
    GPIO.output(inLeft1, GPIO.LOW)
    GPIO.output(inLeft2, GPIO.HIGH)
    
flag_sensor_light = "C"

def follow_line(sign_1, sign_2, sign_3, sign_4, sign_5):
    global flag_sensor_light
    if sign_4 == 1 and sign_5 == 1 and sign_2 == 1 and sign_1 == 1 and sign_3 == 0:
        flag_sensor_light = "C"
    elif sign_4 == 1 and sign_5 == 1 and sign_2 == 0 and sign_1 == 1:
        flag_sensor_light = "L"
    elif sign_4 == 1 and sign_5 == 1 and sign_1 == 0:
        flag_sensor_light = "LM"
    elif sign_4 == 0 and sign_5 == 1 and sign_2 == 1 and sign_1 == 1:
        flag_sensor_light = "R"
    elif sign_5 == 0 and sign_2 == 1 and sign_1 == 1:
        flag_sensor_light = "RM"

while True:
    ret, frame = cap.read()
    key = cv2.waitKey(1)
    cv2.imshow("New Vehicle", frame)
    forward_with_speed(speed)
#     sign_1 = GPIO.input(sensor_1)
#     sign_2 = GPIO.input(sensor_2)
#     sign_3 = GPIO.input(sensor_3)
#     sign_4 = GPIO.input(sensor_4)
#     sign_5 = GPIO.input(sensor_5)
#     print(sign_1, sign_2, sign_3, sign_4, sign_5)
#     follow_line(sign_1, sign_2, sign_3, sign_4, sign_5)
#     
#     print(flag_sensor_light)
#     if flag_sensor_light == "C":
#         forward_with_speed(speed)
#     elif flag_sensor_light == "R":
#         turn_right(10)
#     elif flag_sensor_light == "RM":
#         turn_right_max()
#     elif flag_sensor_light == "L":
#         turn_left(10)
#     elif flag_sensor_light == "LM":
#         turn_left_max()
#     pressButton = GPIO.input(button)
    if(key==ord('q') or pressButton == 0):
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


