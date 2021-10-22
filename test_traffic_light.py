import cv2
# trích suất ảnh từ camera
cap = cv2.VideoCapture(1)
# load model haarcascade
detect_right = cv2.CascadeClassifier('data_traffic_signs/right.xml')
detect_left = cv2.CascadeClassifier('data_traffic_signs/left.xml')
detect_30 = cv2.CascadeClassifier('data_traffic_signs/30.xml')
detect_20 = cv2.CascadeClassifier('data_traffic_signs/20.xml')
detect_stop = cv2.CascadeClassifier('data_traffic_signs/stop.xml')
flag_prioritize = 0
detect = ""
array = {
    'STOP': detect_stop,
    '30': detect_30,
    '20': detect_20,
    'RIGHT': detect_right,
    'LEFT': detect_left
    }
def detect_traffic_sign(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for k, v in array.items():
        detect = v.detectMultiScale(gray, 1.8, 6)
        for (x, y, w, h) in detect:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)  
        if type(detect) != tuple:
            return k
            
    

while (True):
    ret, img = cap.read()
    value = detect_traffic_sign(img)
    if value is not None:
        detect = value
        print(value)
        
    print(detect)
    cv2.imshow('frame', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
