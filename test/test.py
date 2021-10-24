import cv2
from time import sleep
import pigpio
import time
import math
##################
pi = pigpio.pi()
pi.set_servo_pulsewidth(12, 0)    # off
pi.set_servo_pulsewidth(13, 0)    # off
pi.set_servo_pulsewidth(13, 1500)
# pi.set_servo_pulsewidth(12, 1500)
sleep(1.09)
##################
#define speed value
max_speed = 1650 # toc do deba
min_speed = 1600 # toc do chay trung binh
minus_speed = 5 # toc do giam dan

# define turn value
value_turn_right = 1200
value_turn_left = 1800
turn_value = 200

def start_run_forward(maxSpeed, minSpeed, minusSpeed):
    pi.set_servo_pulsewidth(13, maxSpeed)
    while maxSpeed > minSpeed:
        maxSpeed -= minusSpeed
        sleep(0.1)
        pi.set_servo_pulsewidth(13, maxSpeed)
        print(maxSpeed)
    pi.set_servo_pulsewidth(13, maxSpeed)

def turn_left(value):
    pi.set_servo_pulsewidth(12, value)
    
def turn_right(value):
    pi.set_servo_pulsewidth(12, value)

    
                            

cap = cv2.VideoCapture(0)
start_run_forward(max_speed, min_speed, minus_speed)
while True:
    ret, frame = cap.read()
    key = cv2.waitKey(1)
    cv2.imshow("HELloz", frame)
    if(key==ord('q')):
        break
    if(key==ord('n')):
        turn_right(value_turn_right)
    if(key==ord('m')):
        turn_right(value_turn_right - turn_value)
    if(key==ord('b')):
        turn_left(value_turn_left)
    if(key==ord('v')):
        turn_left(value_turn_left + turn_value)
    
# pi.set_servo_pulsewidth(13, 1500)
pi.set_servo_pulsewidth(12, 1500)
cap.release()
pi.set_servo_pulsewidth(13, 0)    # off
pi.set_servo_pulsewidth(12, 0)    # off
pi.stop()
cv2.destroyAllWindows()

