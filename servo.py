import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program
GPIO.setmode(GPIO.BCM) # Sets the pin numbering system to use the physical layout

# Set up  PWM
GPIO.setup(19,GPIO.OUT)  
GPIO.setup(26,GPIO.OUT) 
p = GPIO.PWM(23, 50)  
t = GPIO.PWM(24, 50)   
p.start(0) 
t.start(0)             


# Move the servo back and forth
p.ChangeDutyCycle(8.5)
sleep(1)                 # Wait 1 second
t.ChangeDutyCycle(11.7)
sleep(1)

#happy

t.ChangeDutyCycle(11.5)
sleep(0.2)
t.ChangeDutyCycle(11)
sleep(0.2)
t.ChangeDutyCycle(11.7)
sleep(3)

#sad
p.ChangeDutyCycle(8)
sleep(0.2)
t.ChangeDutyCycle(12.2)
sleep(0.3)
p.ChangeDutyCycle(8.5)            
t.ChangeDutyCycle(11.7)
sleep(3)

#angry
t.ChangeDutyCycle(12.2)
sleep(0.5)
t.ChangeDutyCycle(11.7)
sleep(3)

#disgust

p.ChangeDutyCycle(8.1)
sleep(0.2)
p.ChangeDutyCycle(8.9)
sleep(0.2)
p.ChangeDutyCycle(8.5)
sleep(0.2)


#fear
t.ChangeDutyCycle(11.4)
sleep(0.5)
t.ChangeDutyCycle(11.7)
sleep(3)

