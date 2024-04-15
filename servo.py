import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program
GPIO.setmode(GPIO.BOARD) # Sets the pin numbering system to use the physical layout

# Set up  PWM
GPIO.setup(23,GPIO.OUT)  
p = GPIO.PWM(23, 50)     
p.start(0) 
             

def move(angle):
    duty = 2.5 + (float(angle) / 18)
    p.ChangeDutyCycle(duty)
# Move the servo back and forth
move(30)     # Changes the pulse width to 3 (so moves the servo)
sleep(1)                 # Wait 1 second
move(90)    # Changes the pulse width to 12 (so moves the servo)
sleep(1)

# Clean up everything
p.stop()                 # At the end of the program, stop the PWM
GPIO.cleanup()   