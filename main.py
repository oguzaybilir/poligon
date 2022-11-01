import cv2
import numpy as np
import imutils
import time

path = "/home/oguzay/Documents/GitHub/poligon/src/video.mp4"

cap = cv2.VideoCapture(path)

first_frame = None

while True:

    ret, frame = cap.read()
    framez = frame.copy()

    if cap.isOpened():
            
        if ret:

            framez = cv2.cvtColor(framez, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(framez, (21,21), 0)

            if first_frame is None:
                first_frame = gray
                continue

            frameDelta = cv2.absdiff(first_frame,gray) 
            thresh = cv2.threshold(frameDelta,25,255,cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=5)
            cnts = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)  

            for c in cnts: 

                if cv2.contourArea(c) < 1500:  

                    (x,y,w,h) = cv2.boundingRect(c) 
                    cv2.rectangle(frame,(x,y),(x+w, y+h),(0,0,255),2) 

        cv2.imshow("Security Feed",frame)
        #cv2.imshow("Thresh",thresh)
        #cv2.imshow("Frame Delta",frameDelta)

        key = cv2.waitKey(1000)

        if key == ord("q"):
            print("goruntu kapatiliyor")
            break
    else:
        print("video bittiği icin gosterilebilecek frame kalmadi")
        break

cap.release()
cv2.destroyAllWindows()