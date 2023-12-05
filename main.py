# Import and initialize the pygame library
import pygame
from moviepy.editor import VideoFileClip
import os

pygame.init()
os.environ["DISPLAY"] = ":0"
pygame.display.init()
clip = VideoFileClip("resources/videos/test.mp4")
clip.preview(fullscreen=True)

# Set up the drawing window
screen = pygame.display.set_mode(clip.size, pygame.FULLSCREEN)

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()