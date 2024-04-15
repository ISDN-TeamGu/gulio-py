import pygame
import asyncio
from src.etc.pygamevideo import Video
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
        
        # Set up the display window
        image = pygame.image.load(image_path)

        # Main loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Fill the screen with white
            self.screen.fill((255, 255, 255))

            # Display the image on the screen
            self.screen.blit(image, (0, 0))

            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()

