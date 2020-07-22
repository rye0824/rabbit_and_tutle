# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
time.sleep(1)

while True:
    result = GPIO.input(7)
    if result == 1:
        print("진동이 감지 되었습니다.")
        time.sleep(0.05)
        
    else:
        print("진동이 없습니다.")
        time.sleep(0.05)
