import pygame
import asyncio
from src.etc.pygamevideo import Video
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program
GPIO.setmode(GPIO.BCM) # Sets the pin numbering system to use the physical layout
import src.singleton as singleton

class VideoPlayer:
    def __init__(self):
        info = pygame.display.Info()

        # and create a borderless window that's as big as the entire screen
        self.window = pygame.display.set_mode((1200, 1080), pygame.SCALED | pygame.NOFRAME | pygame.FULLSCREEN)
        # self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.video = None
        

        # Setup singleton
        singleton.video_player = self
        

    def draw(self):
        pygame.event.pump() #MUST KEEP THIS TO PREVENT FREEZING
        if self.video is None:
            return
        self.video.draw_to(self.window, (0, 0))

        # Update pygame display
        pygame.display.flip()
    def play(self, videoPath, loop=True):
        try:
            # Load the video from the specified path
            self.video = Video(videoPath)

            # Start the video
            self.video.play(loop)

            print("playing video: ", self.video.frame_width)
        except:
            print("Error playing video: ", videoPath)
    def stop(self):
        self.video.release()

    def display_image(self, image_path):
    # Initialize Pygame
        try:
            # Set up the display window
            image = pygame.image.load(image_path)

            if hasattr(self, 'image_displayed'):  # Check if image has been displayed before
                # Fill the screen with white
                self.window.fill((255, 255, 255))

            # Display the image on the screen
            self.window.blit(image, (0, 0))

            # Update the display
            pygame.display.flip()

            # Store that an image has been displayed
            self.image_displayed = True
        except:
            print("Error occurred while displaying the image.")
            # Quit Pygame
            pygame.quit()

    def stop_motors(self):
        try:
            GPIO.output(23, GPIO.LOW)  # Set the GPIO pin 23 to LOW
            GPIO.output(24, GPIO.LOW)  # Set the GPIO pin 24 to LOW
            
            # Optionally, if you were using PWM, you can stop the PWM signals:
            # p.stop()
            # t.stop()

        except Exception as e:
            print("An error occurred while stopping the motors:", str(e))

    def move(self, emotion):
        try:
            print("move called")
            GPIO.setup(23,GPIO.OUT)  
            GPIO.setup(24,GPIO.OUT) 
            p = GPIO.PWM(23, 50)  
            t = GPIO.PWM(24, 50)   
            p.start(0) 
            t.start(0)    
            # and create a borderless window that's as big as the entire screen
        
            
            if emotion == "happy":
            #happy
                
                t.ChangeDutyCycle(11.4)
                sleep(0.2)
                t.ChangeDutyCycle(11)
                sleep(0.2)
                t.ChangeDutyCycle(11.8)
                sleep(0.1)
            if emotion == "sad":
            #sad
                p.ChangeDutyCycle(8)
                sleep(0.2)
                t.ChangeDutyCycle(12.5)
                sleep(0.3)
                p.ChangeDutyCycle(8.5) 
                sleep(0.1)           
                t.ChangeDutyCycle(11.8)
                sleep(0.1)
            if emotion == "angry":
            #angry
                t.ChangeDutyCycle(12.5)
                sleep(0.5)
                t.ChangeDutyCycle(11.8)
                sleep(0.1)
                
            if emotion == "disgust":
            #disgust
                
                p.ChangeDutyCycle(8.1)
                sleep(0.2)
                p.ChangeDutyCycle(8.9)
                sleep(0.2)
                p.ChangeDutyCycle(8.5)
                sleep(0.1)
                
            if emotion == "fear":
            #fear
                t.ChangeDutyCycle(11.4)
                sleep(0.5)
                t.ChangeDutyCycle(11.8)
                sleep(0.1)
            self.stop_motors()

        except Exception as e:
            print("An error occurred:", str(e))