from imutils import paths
from picamera.array import PiRGBArray
from picamera import PiCamera
import math
import time
import numpy as np
import imutils
import cv2
import RPi.GPIO as GPIO
vib_pin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(vib_pin, GPIO.OUT)
pwm_vib = GPIO.PWM(vib_pin, 500)
pwm_vib.start(100)


def find_marker(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #make mono
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 35, 125)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key = cv2.contourArea)
    return cv2.minAreaRect(c)
def distance_to_camera(knownWidth, focalLength, perWidth):
    return (knownWidth * focalLength) / perWidth

    
def vib(distance):
    if(distance > 60.0):
        pwm_vib.ChangeDutyCycle(0)
    elif(distance > 40.0):
        pwm_vib.ChangeDutyCycle(35)
    elif(distance > 20.0):
        pwm_vib.ChangeDutyCycle(70)
    else :
        pwm_vib.ChangeDutyCycle(100)
    
vib(0)


#cvcam.py start
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(1)

KNOWN_DISTANCE = 30.0
KNOWN_WIDTH = 3.0

while(True):
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array

        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("q"):
            break
        cv2.imwrite("/home/pi/testimage.png",image)
        time.sleep(1)
        cv2.imwrite("/home/pi/data/image0.png",image)
        time.sleep(1)
        cv2.imwrite("/home/pi/data/image1.png",image)
        time.sleep(0.1)
        
    
    img = cv2.imread("/home/pi/testimage.png")
    marker = find_marker(image)
    focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

    for imagePath in sorted(paths.list_images("/home/pi/data")):
        img = cv2.imread(imagePath)
        marker = find_marker(image)
        dis = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
        box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
        box = np.int0(box)
        cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
        cv2.ellipse(image, (image.shape[1] - 100, image.shape[0] - 30),(100,25),0,0,360,(255,255,255),-1)
 
        cv2.putText(image, "%.2fcm" % (dis),
            (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 3)
        cv2.imshow("image", image)
        x = box[0][0]- box[1][0]
        y = box[0][1]- box[1][1]
        vib(dis)
        KNOWN_DISTANCE = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
        KNOWN_WIDTH = math.sqrt((x*x)+(y*y))
        continue
        

