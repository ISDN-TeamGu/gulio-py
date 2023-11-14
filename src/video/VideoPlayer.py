
from pygamevideo import Video

class VideoPlayer:
    def __init__(self):
        self.current_video = None

    def play(self, videoPath):
        # Stop the current video
        if self.current_video is not None:
            self.current_video.stop()

        # Load the video from the specified dir
        self.current_video = Video(videoPath)

        # Start the video
        self.current_video.play()
    
    def draw_to(self, surface, position):
        # Draw the video to the specified surface
        if self.current_video is not None:
            self.current_video.draw_to(surface, position)

