import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

render = SimpleMFRC522()

try:
    id, text = render.read()
    print(id)
    print(text)
finally:
    GPIO.cleanup()