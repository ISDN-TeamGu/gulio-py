# Import and initialize the pygame library
import pygame
from src.video.VideoPlayer import *
from TTS.test import *
import numpy as np
import asyncio
import simpleaudio as sa
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

videoPlayer = VideoPlayer()
videoPlayer.play("./resources/videos/test.mp4")
#function to call playht
asyncio.run(AIvoice.async_main(user="w67Bc740ToecfLroYCRQ2Dw042I3",key="7e684a86098e48359d38cc536e8b5769",text=["You are harry potter"],quality="faster",interactive=False,use_async=True,voice="s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json"))
# Run until the user asks to quit
running = True
while running:

     #Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw video to display surface
    videoPlayer.draw_to(screen, (screen.get_width()/4, screen.get_height()/5))

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()