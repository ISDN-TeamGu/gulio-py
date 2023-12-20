import RPi.GPIO as GPIO
from mfrc522 import MFRC522
from mfrc522 import SimpleMFRC522
reader = MFRC522()
import threading


def detect_rfid():
    try:
        while True:
            status, _ = reader.MFRC522_Request(reader.PICC_REQIDL)
            if status != reader.MI_OK:
                sleep(0.1)
                continue
            status, backData = reader.MFRC522_Anticoll()
            buf = reader.MFRC522_Read(0)
            reader.MFRC522_Request(reader.PICC_HALT)
            if buf:
                print(datetime.now().isoformat(), ':'.join([hex(x) for x in buf]))
                start_main_process_thread()
                break
    finally:
            GPIO.cleanup()
t = threading.Thread(target=detect_rfid)
t.daemon = True
t.start()

from datetime import datetime
from time import sleep
from main import *

# start_main_process_thread() # Remove this for raspberry pi
start_rendering()