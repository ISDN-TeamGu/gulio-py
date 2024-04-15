import pygame
import asyncio
from src.etc.pygamevideo import Video
import src.singleton as singleton

class ImageDisplaySingleton:
    __instance = None

    @staticmethod
    def get_instance():
        if ImageDisplaySingleton.__instance is None:
            ImageDisplaySingleton()
        return ImageDisplaySingleton.__instance

    def __init__(self):
        if ImageDisplaySingleton.__instance is not None:
            raise Exception("ImageDisplaySingleton is a singleton class. Use get_instance() to access the instance.")
        else:
            # Initialize Pygame
            pygame.init()

            # Set up the display window
            self.screen = pygame.display.set_mode((800, 600))
            pygame.display.set_caption("Image Display")

            # Track the current image path
            self.image_path = ""

            ImageDisplaySingleton.__instance = self

    def display_image(self, image_path):
        # Load the image
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
