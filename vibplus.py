import RPi.GPIO as GPIO
import time

vib_pin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(vib_pin, GPIO.OUT)

pwm_vib = GPIO.PWM(vib_pin, 500)
pwm_vib.start(100)

while True:
    duty = 0
    while duty < 101:
        print("duty : "+str(duty))
        time.sleep(2)
        pwm_vib.ChangeDutyCycle(duty)
        duty = duty + 10
    
    end_key = input(" - Stop to Vibrate Motor , Please enter the 'end' : ")
    if end_key == "end":
        break
    
GPIO.cleanup()     
