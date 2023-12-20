import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

render = SimpleMFRC522()

try:
    text = input("New data: ")
    print("Now place your tag to write")
    render.write(text)
    print("Written")
finally:
    GPIO.cleanup()