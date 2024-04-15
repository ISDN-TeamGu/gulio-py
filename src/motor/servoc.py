import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program
GPIO.setmode(GPIO.BCM) # Sets the pin numbering system to use the physical layout
import src.singleton as singleton

class Motor:
    def __init__(self):
        GPIO.setup(23,GPIO.OUT)  
        GPIO.setup(24,GPIO.OUT) 
        p = GPIO.PWM(23, 50)  
        t = GPIO.PWM(24, 50)   
        p.start(0) 
        t.start(0)    
        # and create a borderless window that's as big as the entire screen
        
        p.ChangeDutyCycle(8.5)
        sleep(1)                 # Wait 1 second
        t.ChangeDutyCycle(11.8)
        sleep(1)

        # Setup singleton
        singleton.motor = self


    def move(self, emotion):
    # Initialize Pygame
        try:
            if emotion == "happy":
            #happy
                t.ChangeDutyCycle(12.2)
                sleep(1)
                t.ChangeDutyCycle(11.8)
                sleep(0.2)
                t.ChangeDutyCycle(11.4)
                sleep(0.2)
                t.ChangeDutyCycle(11)
                sleep(0.2)
                t.ChangeDutyCycle(10.6)
                sleep(0.2)
                t.ChangeDutyCycle(11.8)
                sleep(3)
            if emotion == "sad":
            #sad
                p.ChangeDutyCycle(8)
                sleep(0.2)
                t.ChangeDutyCycle(12.5)
                sleep(1.5)
                p.ChangeDutyCycle(8.5)            
                t.ChangeDutyCycle(11.8)
                sleep(3)
            if emotion == "angry":
            #angry
                t.ChangeDutyCycle(12.5)
                sleep(2)
                t.ChangeDutyCycle(11.8)
                sleep(3)
            if emotion == "disgust":
            #disgust
                t.ChangeDutyCycle(11.4)
                sleep(0.2)
                p.ChangeDutyCycle(8.1)
                sleep(0.2)
                p.ChangeDutyCycle(8.9)
                sleep(0.2)
                p.ChangeDutyCycle(8.1)
                sleep(0.2)
                p.ChangeDutyCycle(8.5)
                sleep(0.2)
                t.ChangeDutyCycle(11.8)
                sleep(3)
            if emotion == "fear":
            #fear
                t.ChangeDutyCycle(11.4)
                sleep(2)
                t.ChangeDutyCycle(11.8)
                sleep(3)

        except:
            print("Error occurred")
            