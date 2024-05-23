import pygame
import asyncio
from src.etc.pygamevideo import Video
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program
GPIO.setmode(GPIO.BCM) # Sets the pin numbering system to use the physical layout
import src.singleton as singleton
from button import *
BG = pygame.image.load("assets/Background.jpg")
response = "" 
class VideoPlayer:
    def __init__(self):
        info = pygame.display.Info()

        # and create a borderless window that's as big as the entire screen
        rotated_surface = pygame.Surface((1200, 1000))
        rotated_surface = pygame.transform.rotate(rotated_surface, 90)

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
    
    def home(self, line1, line2):
        while True:
            self.window.blit(BG, (0, 0))
    
            MENU_MOUSE_POS = pygame.mouse.get_pos()
    
            
    
            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                                text_input=line1, font=get_font2(130), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 550), 
                                text_input=line2, font=get_font2(130), base_color="#d7fcd4", hovering_color="White")
            
    
    
            for button in [PLAY_BUTTON, OPTIONS_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.window)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        response = line1
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        response = line2 
                    
            pygame.display.update()
    def display_image(self, image_path):
    # Initialize Pygame
        try:
            # Set up the display window
            image = pygame.image.load(image_path)
            # Get the rect of the rotated image
            rotated_rect = image.get_rect()

            # Calculate the position to center the rotated image
            x = (1200 - rotated_rect.width) // 2
            y = (1000 - rotated_rect.height) // 2

            if hasattr(self, 'image_displayed'):  # Check if image has been displayed before
                # Fill the screen with white
                self.window.fill((255, 255, 255))

            # Display the image on the screen
            self.window.blit(image, (x, y))

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
            GPIO.output(19, GPIO.LOW)  # Set the GPIO pin 23 to LOW
            GPIO.output(26, GPIO.LOW)  # Set the GPIO pin 24 to LOW
            
            # Optionally, if you were using PWM, you can stop the PWM signals:
            # p.stop()
            # t.stop()

        except Exception as e:
            print("An error occurred while stopping the motors:", str(e))

    def move(self, emotion):
        try:
            print("move called")
            GPIO.setup(19,GPIO.OUT)  
            GPIO.setup(26,GPIO.OUT) 
            p = GPIO.PWM(26, 50)  
            t = GPIO.PWM(19, 50)   
            p.start(0) 
            t.start(0)    
            # and create a borderless window that's as big as the entire screen
        
            
            if emotion == "happy":
            #happy
                
                t.ChangeDutyCycle(11.3)
                sleep(0.2)
                t.ChangeDutyCycle(11.5)
                sleep(0.2)
                t.ChangeDutyCycle(11.7)
                sleep(0.1)
            if emotion == "sad":
            #sad
                p.ChangeDutyCycle(8)
                sleep(0.2)
                t.ChangeDutyCycle(11.4)
                sleep(0.3)
                p.ChangeDutyCycle(8.5) 
                sleep(0.1)           
                t.ChangeDutyCycle(11.7)
                sleep(0.1)
            if emotion == "angry":
            #angry
                t.ChangeDutyCycle(12)
                sleep(0.5)
                t.ChangeDutyCycle(11.7)
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
                t.ChangeDutyCycle(11.2)
                sleep(0.5)
                t.ChangeDutyCycle(11.7)
                sleep(0.1)
            #self.stop_motors()

        except Exception as e:
            print("An error occurred:", str(e))
