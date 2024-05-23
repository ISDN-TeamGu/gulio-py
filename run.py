import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program
GPIO.setmode(GPIO.BCM) # Sets the pin numbering system to use the physical layout

# Set up  PWM
GPIO.setup(19,GPIO.OUT)  
GPIO.setup(26,GPIO.OUT) 
p = GPIO.PWM(19, 50)  
t = GPIO.PWM(26, 50)   
p.start(0) 
t.start(0)             


# Move the servo back and forth
p.ChangeDutyCycle(8.5)
sleep(1)                 # Wait 1 second
t.ChangeDutyCycle(12)
sleep(1)
