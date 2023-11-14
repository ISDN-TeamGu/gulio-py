# Import and initialize the pygame library
import pygame
from src.video.VideoPlayer import *

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

videoPlayer = VideoPlayer()
videoPlayer.play("./resources/videos/test.mp4")

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw video to display surface
    videoPlayer.draw_to(screen, (screen.get_width()/4, screen.get_height()/5))

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()