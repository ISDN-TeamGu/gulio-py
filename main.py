# Import and initialize the pygame library
import pygame
import os
from src.video.VideoPlayer import VideoPlayer
from src.command.CommandProcessor import CommandProcessor
from multiprocessing import Process
import asyncio
import threading
import src.singleton as singleton


pygame.init()
os.environ["DISPLAY"] = ":0"
pygame.display.init()

# SETUP SINGLETONS
command_processor = CommandProcessor()
video_player = VideoPlayer()

time = 0
loop_interval = 10

video_player.play("resources/videos/test.mp4")


# Processing Command
def command_prompt():
    while True:
        response = input('Please enter the command: ')
        command_processor.run_command(response)


thread2 = threading.Thread(target=command_prompt)
thread2.start()



# Drawing Display
while True:
    pygame.time.wait(30)
    video_player.draw()

