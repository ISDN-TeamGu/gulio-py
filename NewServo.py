import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, pin):
        self.current_angle = None
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, 50)
        self.pwm.start(0)

    def __angle_to_duty(self, angle):
        duty_0 = 2.5
        duty_180 = 12.5
        return duty_0 + (float(angle) / 180) * (duty_180 - duty_0)

    def move(self, angle, speed):
        # round to 2 decimal places, so we have a chance of reducing unwanted servo adjustments
        angle = round(angle, 2)
        # do we need to move?
        if angle == self.current_angle:
            return
        self.current_angle = angle
        # calculate the new duty cycle and move the motor
        duty = self.__angle_to_duty(angle)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(speed)

