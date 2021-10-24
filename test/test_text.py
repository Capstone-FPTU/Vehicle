import pytesseract
import cv2

cap = cv2.VideoCapture(0)
count = 0
while True:
    _, img = cap.read()
    key = cv2.waitKey(1)
    text = pytesseract.image_to_string(img, 'eng')
    
    print(text, count)
    if text is not None:
        count += 1
        print(text, count)
    
    cv2.imshow("Image", img)
    if key == ord("q"):
        break
    
cv2.destroyAllWindows()
