import cv2

cap = cv2.VideoCapture(0)

while True:
    _, img = cap.read()
    key = cv2.waitKey(1)
    cv2.imshow("img",img)
    if key == ord("q"):
        break
    
cv2.destroyAllWindows();
    