from sg90 import Servo
import time


motor1=Servo(pin=14)
motor2=Servo(pin=15)
motor2.move(90)
motor1.move(90)

time.sleep(0.3)
motor1.move(50)
time.sleep(0.3)
motor1.move(40)
time.sleep(0.3)
motor1.move(30)
time.sleep(0.3)
motor1.move(40)
time.sleep(0.3)
motor1.move(50)
time.sleep(0.3)
motor1.move(40)
time.sleep(0.3)
motor1.move(30)
time.sleep(0.3)
motor1.move(40)
time.sleep(0.3)
motor1.move(90)
time.sleep(0.5)
motor2.move(60)
time.sleep(0.5)
motor2.move(90)