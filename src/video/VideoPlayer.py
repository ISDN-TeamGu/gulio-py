import pygame
import asyncio
from pygamevideo import Video

class VideoPlayer:
    def __init__(self):
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.video = None

    def draw(self):
        if self.video is None:
            return
        # Draw video to display surface
        print("drawing")
        # this function should be called every frame
        self.video.draw_to(self.window, (0, 0))

        # Update pygame display
        pygame.display.flip()
    def play(self, videoPath):
        # Load the video from the specified path
        self.video = Video(videoPath)

        # Start the video
        self.video.play()

        print("playing video: ", self.video.frame_width)