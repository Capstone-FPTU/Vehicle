import cv2
import numpy as np
import pytesseract
cap = cv2.VideoCapture(0)
area = 0
while(1):

    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # RGB to Gray scale conversion
    img_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

  # Noise removal with iterative bilateral filter(removes noise while preserving edges)
    noise_removal = cv2.bilateralFilter(img_gray,9,75,75)

  # Histogram equalisation for better results
    equal_histogram = cv2.equalizeHist(noise_removal)


  # Morphological opening with a rectangular structure element
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    morph_image = cv2.morphologyEx(equal_histogram,cv2.MORPH_OPEN,kernel,iterations=15)

  # Image subtraction(Subtracting the Morphed image from the histogram equalised Image)
    sub_morp_image = cv2.subtract(equal_histogram,morph_image)

  # Thresholding the image
    ret,thresh_image = cv2.threshold(sub_morp_image,0,255,cv2.THRESH_OTSU)


  # Applying Canny Edge detection
    canny_image = cv2.Canny(thresh_image,250,255)

    canny_image = cv2.convertScaleAbs(canny_image)

  # dilation to strengthen the edges
    kernel = np.ones((3,3), np.uint8) 
  # Creating the kernel for dilation
    dilated_image = cv2.dilate(canny_image,kernel,iterations=1)

  # Finding Contours in the image based on edges
    contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours= sorted(contours, key = cv2.contourArea, reverse = True)[:10]
  # Sort the contours based on area ,so that the number plate will be in top 10 contours
    screenCnt = None
  # loop over our contours
    loop = 1
    for c in contours:
        print ("loop #: " + str(loop))
        loop = loop+1
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.06 * peri, True)  # Approximating with 6% error
        print ("approx: " + str(len(approx)))
        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) == 4:  # Select the contour with 4 corners
          screenCnt = approx
          top_left = approx[0][0] #[x y]
          top_right = approx[1][0]
          bottom_left = approx[2][0]
          bottom_right = approx[3][0]
        
          top_idx = min(top_left[1], top_right[1])
          bottom_idx = max(bottom_left[1], bottom_right[1])
          left_idx=min(min(top_left[0], top_right[0]),min(bottom_left[0], bottom_right[0]))
          right_idx=max(max(top_left[0], top_right[0]),max(bottom_left[0], bottom_right[0]))

          print ("Yay, find one")
          break
    ## Masking the part other than the number plate
    mask = np.zeros(img_gray.shape,np.uint8)
    new_image = cv2.drawContours(mask,[screenCnt],0,255,3)
    new_image = cv2.bitwise_and(frame,frame,mask=mask)

  # Histogram equal for enhancing the number plate for further processing
    y,cr,cb = cv2.split(cv2.cvtColor(new_image,cv2.COLOR_BGR2YCR_CB))
  # Converting the image to YCrCb model and splitting the 3 channels
    y = cv2.equalizeHist(y)
  # Applying histogram equalisation
    final_image = cv2.cvtColor(cv2.merge([y,cr,cb]),cv2.COLOR_YCR_CB2BGR)
  # Merging the 3 channels

  #cv2.namedWindow("12_Extract",cv2.WINDOW_NORMAL)
  #print(new_image.shape)
    final_new_image = new_image[top_idx:bottom_idx,left_idx:right_idx ]
    print(final_new_image.shape)
  #cv2.imshow("12_Extract", final_new_image)

    cv2.imwrite('result1.jpg',new_image)
    cv2.imwrite('result2.jpg',final_new_image)

    im = final_new_image
    im[np.where((im <[20,20,20]).all(axis = 2))] = [255,255,255]

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 6))
    binl = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
    open_out = cv2.morphologyEx(binl, cv2.MORPH_OPEN, kernel)
    cv2.bitwise_not(open_out, open_out)
  #cv2.namedWindow("Transfered",cv2.WINDOW_NORMAL)
  #cv2.imshow("Transfered", open_out)
    cv2.imwrite('output1.jpg', open_out)
#     if len(contours) != 0:
#         for contour in contours:
#             approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
#             
#             if len(contour) == 3:
#                 
#                 cv2.drawContours(frame,[approx], 0, (0), 5);
#                 if cv2.contourArea(contour) > 500:
#                     x, y, w, h = cv2.boundingRect(contour)
#                     cv2.rectangle(frame, (x,y), (x+ w, y +h), (0,0,255), 3)
#                     crop_img = frame[y:y + h, x:x + w]
#                     if w > h :
#                         cv2.imshow("cropped", crop_img)
#                         text = pytesseract.image_to_string(crop_img)
#                         print(text)
#                         if "HO" in text:
#                             print('toi noi')

    # Bitwise-AND mask and original image
#     res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('frame',frame)
#     cv2.imshow('mask',mask)
#     cv2.imshow('res',res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
