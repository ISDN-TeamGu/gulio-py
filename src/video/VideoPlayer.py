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
    
    def home(self):
        button_width = 200
        button_height = 50
        button_color = (0, 255, 0)
        button_hover_color = (0, 200, 0)

        # Create the first button
        button1_x = (1200 / 2) - (button_width / 2)
        button1_y = (1000 / 2) - (button_height / 2) - 50
        button1_rect = pygame.Rect(button1_x, button1_y, button_width, button_height)
        button1_text = "Button 1"
        button1_font = pygame.font.Font(None, 36)
        button1_surface = button1_font.render(button1_text, True, (255, 255, 255))
        button1_hover = False

        # Create the second button
        button2_x = (1200 / 2) - (button_width / 2)
        button2_y = (1000 / 2) - (button_height / 2) + 50
        button2_rect = pygame.Rect(button2_x, button2_y, button_width, button_height)
        button2_text = "Button 2"
        button2_font = pygame.font.Font(None, 36)
        button2_surface = button2_font.render(button2_text, True, (255, 255, 255))
        button2_hover = False
        try:
            self.window.fill((255, 255, 255))
            # Set the button dimensions and colors
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = event.pos
                    if button1_rect.collidepoint(mouse_pos):
                        button1_hover = True
                    else:
                        button1_hover = False
                    if button2_rect.collidepoint(mouse_pos):
                        button2_hover = True
                    else:
                        button2_hover = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if button1_rect.collidepoint(mouse_pos):
                        print("Button 1 clicked!")
                    elif button2_rect.collidepoint(mouse_pos):
                        print("Button 2 clicked!")

        # Draw the buttons
            if button1_hover:
                pygame.draw.rect(screen, button_hover_color, button1_rect)
            else:
                pygame.draw.rect(screen, button_color, button1_rect)
            screen.blit(button1_surface, (button1_x + 10, button1_y + 10))

            if button2_hover:
                pygame.draw.rect(screen, button_hover_color, button2_rect)
            else:
                pygame.draw.rect(screen, button_color, button2_rect)
            screen.blit(button2_surface, (button2_x + 10, button2_y + 10))

            # Update the screen
            pygame.display.flip()

        # Quit Pygame
            pygame.quit()
   
        except:
            print("Error occurred while displaying home screen")
            # Quit Pygame
            pygame.quit()

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
