import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program
GPIO.setmode(GPIO.BCM) # Sets the pin numbering system to use the physical layout

# Set up  PWM
GPIO.setup(23,GPIO.OUT)  
GPIO.setup(24,GPIO.OUT) 
p = GPIO.PWM(23, 50)  
t = GPIO.PWM(24, 50)   
p.start(0) 
t.start(0)             


# Move the servo back and forth
p.ChangeDutyCycle(8.5)
sleep(1)                 # Wait 1 second
t.ChangeDutyCycle(11.8)
sleep(1)

#happy
t.ChangeDutyCycle(12.5)
sleep(1)
t.ChangeDutyCycle(11.8)
sleep(1)
t.ChangeDutyCycle(11.7)
sleep(1)
t.ChangeDutyCycle(11.6)
sleep(1)
t.ChangeDutyCycle(11.4)
sleep(1)
t.ChangeDutyCycle(11.8)
sleep(3)

"""#sad
p.ChangeDutyCycle(8)
t.ChangeDutyCycle(12.5)
p.ChangeDutyCycle(8.5)            
t.ChangeDutyCycle(11.8)
sleep(3)

#angry
t.ChangeDutyCycle(12.5)
t.ChangeDutyCycle(11.8)
sleep(3)

#disgust
t.ChangeDutyCycle(11.4)
p.ChangeDutyCycle(8.3)
p.ChangeDutyCycle(8.7)
p.ChangeDutyCycle(8.3)
p.ChangeDutyCycle(8.5)
t.ChangeDutyCycle(11.8)
sleep(3)

#fear
t.ChangeDutyCycle(11.4)
sleep(2)
t.ChangeDutyCycle(11.8)
"""
