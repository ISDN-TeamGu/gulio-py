from NewServo import Servo
import time# Create a servo instance
servo = Servo(18)

# Move the servo to 0 degrees at slow speed
servo.move(0, 0.1)

# Move the servo to 90 degrees at medium speed
servo.move(30, 0.05)

# Move the servo to 180 degrees at fast speed
servo.move(50, 0.02)

# Cleanup
servo.pwm.stop()
GPIO.cleanup()