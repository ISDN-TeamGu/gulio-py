from pyvidplayer2 import Video

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
    
    def draw_to(self, pygame, surface, position):
        # Draw the video to the specified surface
        if self.current_video is not None:
            # Quit when pygame quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.current_video.stop()
            
            # Draw the video
            if self.current_video.draw(surface, position, force_draw=False):
                pygame.display.update()

            # Wait for the next frame
            pygame.time.wait(16) # around 60 fps

