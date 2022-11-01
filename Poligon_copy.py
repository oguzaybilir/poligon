import cv2
import numpy as np
import imutils
import time 

cap = cv2.VideoCapture("C:/Users/busra/OneDrive/Belgeler/GitHub/Okuyar_Gorev/Poligon/Video/video.mp4")


#img = cv2.imread("C://Users//busra//OneDrive//Belgeler//GitHub//Okuyar_Gorev//Poligon//Images//poligon.jpeg")
while 1:
    # Capture two frames
    ret, frame1 = cap.read()  # first image
    time.sleep(1/25)          # slight delay
    ret, frame2 = cap.read()  # second image 
    #img1 = cv2.absdiff(frame1,frame2)  # image difference

    img = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    ret , thresh = cv2.threshold(img,0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    cv2.imshow("thresh", thresh)
    kernel_close = np.ones((3,3),np.uint8)
    kernel_opening = np.ones((3,3),np.uint8)

    close = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel_close,iterations=1)
    opening = cv2.morphologyEx(close,cv2.MORPH_OPEN, kernel_opening,iterations=1)
    cv2.imshow("opening", opening)

    cnts = cv2.findContours(opening.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    daire_contur = []

    for (i,c) in enumerate(cnts):

        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        w,h = img.shape
        sensi = 60
        area_sart = 200

        centerx, centery = w//2, h//2
        centerx1, centery1, centerx2, centery2 = centerx - sensi, centery - sensi, centerx + sensi, centery + sensi
        print("centerx,centery  ", centerx,centery)
        print("centerx1, centery1, centerx2, centery2  ",centerx1, centery1, centerx2, centery2)
        print("cX,cY",cX,cY)
        area = cv2.contourArea(c)

        if centerx1 < cX < centerx2 and centery1 < cY < centery2 and area > area_sart:

            daire_contur.append(c)
            print("daire bulundu")
            cv2.drawContours(img, [c], -1, (0, 0, 255), 4)
            cv2.circle(img, (cX, cY), 7, (255, 0, 0), -1)
        idx = "{}:".format(i)
        print("idx",idx)

    if ret == True:
        cv2.imshow("frame", img) 
        if cv2.waitKey(10000) & 0xFF == ord("q"):
            break

cap.release()

cv2.destroyAllWindows()



