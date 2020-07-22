import RPi.GPIO as GPIO
vib_pin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(vib_pin, GPIO.OUT)

pwm_vib = GPIO.PWM(vib_pin, 500)
pwm_vib.start(100)

while True:
    duty_str = raw_input("Enter Brightness (0 to 100):")
    duty = int(duty_str)
    
    if duty > 100:
        print("wrong input value.")
    else:
        pwm_vib.ChangeDutyCycle(duty)
        end_key = raw_input(" - Stop to Blink LED, Please enter the 'end' : ")
        if end_key == "end":
            break
        

