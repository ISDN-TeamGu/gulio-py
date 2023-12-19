import src.singleton as singleton
from src.video.VideoPlayer import *
class CommandProcessor:
    def __init__(self):
        self.processRate = 1.0
        singleton.command_processor = self
    
    def run_command(self, commandLine):
        # Split the command line into command and arguments
        command_tokens = commandLine.split()
        command = command_tokens[0]
        arguments = command_tokens[1:]
        
        # Check the command and perform the corresponding action
        if command == "play_music":
            self.play_music(arguments)
        elif command == "play_emoji":
            self.play_emoji(arguments)
        elif command == "quit":
            self.quit()
        else:
            print("Unknown command:", command)
    def speak(self, arguments):
        # Handle the playMusic command with its arguments
        if len(arguments) == 0:
            print("Playing music...")
        else:
            song_name = arguments[0]
            print("Playing music:", song_name)
    def play_emoji(self, arguments):
        # Handle the playMusic command with its arguments
        if len(arguments) == 1:
            emoji_name = arguments[0]
            print("Playing emoji:", emoji_name)
            singleton.video_player.play("resources/videos/gulio "+emoji_name+".mp4")
    
    def play_music(self, arguments):
        # Handle the playMusic command with its arguments
        if len(arguments) == 0:
            print("Playing music...")
        else:
            song_name = arguments[0]
            print("Playing music:", song_name)
    
    def quit(self):
        # Handle the quit command
        print("Quitting...")
        # Add your code here to perform any necessary cleanup or termination actions