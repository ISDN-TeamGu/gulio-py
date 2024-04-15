import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program
GPIO.setmode(GPIO.BOARD) # Sets the pin numbering system to use the physical layout

# Set up  PWM
GPIO.setup(23,GPIO.OUT)  
GPIO.setup(24,GPIO.OUT) 
p = GPIO.PWM(23, 50)  
t = GPIO.PWM(24, 50)   
p.start(0) 
t.start(0)             


# Move the servo back and forth
p.ChangeDutyCycle(12.5)
sleep(1)                 # Wait 1 second
p.ChangeDutyCycle(2.5)    # Changes the pulse width to 12 (so moves the servo)
sleep(1)

# Clean up everything
p.stop()                 # At the end of the program, stop the PWM
GPIO.cleanup()   