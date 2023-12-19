# Import and initialize the pygame library
import pygame
import os
from src.video.VideoPlayer import VideoPlayer
from multiprocessing import Process

pygame.init()
os.environ["DISPLAY"] = ":0"
pygame.display.init()
videoPlayer = VideoPlayer()

time = 0
loop_interval = 10

videoPlayer.play("resources/videos/test.mp4")

# Run until the user asks to quit
running = True
while running:
    running = True
    videoPlayer.draw()
    pygame.time.wait(loop_interval)  # Limit the speed of the loop
    time += loop_interval
    if time >= 5000 and time < 5010:
        videoPlayer.play("resources/videos/1211.mp4")