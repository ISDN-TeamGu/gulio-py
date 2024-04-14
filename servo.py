import RPi.GPIO as GPIO
import time

# Set GPIO mode and disable warnings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Configure GPIO pin
servo_pin = 18
GPIO.setup(servo_pin, GPIO.OUT)

# Create PWM object
pwm = GPIO.PWM(servo_pin, 50)  # Set PWM frequency to 50Hz (standard for servos)

# Define servo angles and corresponding duty cycles
angle_0 = 0
duty_0 = 2.5  # Adjust this value to set the minimum duty cycle for your servo
angle_180 = 180
duty_180 = 12.5  # Adjust this value to set the maximum duty cycle for your servo

# Function to set servo angle
def set_angle(angle):
    duty = duty_0 + (float(angle) / (angle_180 - angle_0)) * (duty_180 - duty_0)
    pwm.ChangeDutyCycle(duty)

# Rotate the servo to 0 degrees
set_angle(0)
time.sleep(1)

# Rotate the servo to 90 degrees
set_angle(20)
time.sleep(1)

# Rotate the servo to 180 degrees
set_angle(30)
time.sleep(1)

# Rotate the servo back to 0 degrees
set_angle(0)

# Cleanup
pwm.stop()
GPIO.cleanup()