import cv2
import re
import datetime
from time import sleep
import RPi.GPIO as GPIO


cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()
isOpen = False
sec = 0
time_close = 5
relay = 3
button = 4
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)
GPIO.setup(button, GPIO.IN)
GPIO.output(relay, GPIO.LOW)

while True:
    _, img = cap.read()
    data, bbox, _ = detector.detectAndDecode(img)
    currentDT = datetime.datetime.now()
    if bbox is not None:
        for i in range(len(bbox)):
            cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,0, 0), thickness=2)  
            cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
            
            if data == "Loc Shadow":
                sec = currentDT.second + time_close
                print (currentDT)
                print("Data found: " + data)
                print("Open")
                GPIO.output(relay,GPIO.HIGH)
                data = ""
                isOpen = True
          
    if isOpen:
        if sec > 60:
            sec = sec % 60
        if sec == currentDT.second:
            isOpen = False
            GPIO.output(relay, GPIO.LOW)
            print (currentDT)
            print("Sau 5s Close")
    
    cv2.imshow("code detector", img) 
    if cv2.waitKey(1) == ord("q"):
        break

cap.read()
cv2.destroyAllWindows()