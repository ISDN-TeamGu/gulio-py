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
        GPIO.setup(23,GPIO.OUT)  
        GPIO.setup(24,GPIO.OUT) 
        self.p = GPIO.PWM(23, 50)  
        self.t = GPIO.PWM(24, 50)   
        self.p.start(0) 
        self.t.start(0)  
        
        

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
    def start(self):
        try:
            self.p.ChangeDutyCycle(8.5)
            sleep(1)                 # Wait 1 second
            self.t.ChangeDutyCycle(11.8)
            sleep(1)
            self.stop()
            print("motor initialized")
        except:
            print("error initalizing")
    def stop(self):
        self.p.pwm.stop() 
        self.t.pwm.stop() 
           
    def move(self, emotion):
        try:
            print("move called")
              
            # and create a borderless window that's as big as the entire screen
        
            
            if emotion == "happy":
            #happy
                
                self.t.ChangeDutyCycle(11.4)
                sleep(0.2)
                self.t.ChangeDutyCycle(11)
                sleep(0.2)
                self.t.ChangeDutyCycle(11.8)
                sleep(0.1)
                self.stop
            if emotion == "sad":
            #sad
                self.p.ChangeDutyCycle(8)
                sleep(0.2)
                self.t.ChangeDutyCycle(12.5)
                sleep(0.3)
                self.p.ChangeDutyCycle(8.5) 
                sleep(0.1)           
                self.t.ChangeDutyCycle(11.8)
                sleep(0.1)
            if emotion == "angry":
            #angry
                self.t.ChangeDutyCycle(12.5)
                sleep(0.5)
                self.t.ChangeDutyCycle(11.8)
                sleep(0.1)
                self.stop

                
            if emotion == "disgust":
            #disgust
                
                self.p.ChangeDutyCycle(8.1)
                sleep(0.2)
                self.p.ChangeDutyCycle(8.9)
                sleep(0.2)
                self.p.ChangeDutyCycle(8.5)
                sleep(0.1)
                self.stop
                
            if emotion == "fear":
            #fear
                self.t.ChangeDutyCycle(11.4)
                sleep(0.5)
                self.t.ChangeDutyCycle(11.8)
                sleep(0.1)
                self.stop
            GPIO.cleanup()
        except:
            print("Error occurred")
            