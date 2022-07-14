# Non funziona!!!
# How to get the latest frame from capture device (camera) in opencv
# get_the_latest_frame_from_capture_device_camera_in_opencv.py
import threading
import time
import cv2

#cap = cv2.VideoCapture('rtsp://192.168.0.129')
cap = cv2.VideoCapture('http://admin:a211256ntimo@192.168.1.129/video.cgi?.mjpg') # funziona. Problemi con cv2.imshow('frame', frame)
#cap = cv2.VideoCapture(0) # Funziona. Fa le foto!  Ma vede la mia webcam.
# http://admin:a211256ntimo@192.168.1.129/video.cgi?.mjpg
cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
counter = 0

while True:
   ret, frame = cap.read()
   if ret:
       cv2.imwrite(str(counter) + '.jpg', frame)
       counter = counter + 1
   time.sleep(1)
