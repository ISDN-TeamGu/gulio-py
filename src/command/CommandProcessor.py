import src.singleton as singleton
from src.video.VideoPlayer import *
from src.video.ImageDisplaySingleton import *
from src.motor.servoc import *
from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play


import sys
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

    def playsfx(self, filepath):
        audio = AudioSegment.from_file(filepath)  # Load the audio file
        play(audio) 
    def play_emoji(self, name, emotion):

        # Handle the playMusic command with its arguments
        if name.lower() == "harry" or name.lower() == "dumbledore" or name.lower() == "ron" or name.lower() == "hermione" or name.lower() == "snape":
            emoji_name = name
            emoji = emotion
            print("Playing emoji:", emoji_name)
            singleton.video_player.display_image("resources/videos/emojis/"+emoji_name.lower()+"/"+emoji.lower()+".jpg") 
        elif name.lower() == "narration":
            singleton.video_player.display_image("resources/videos/emojis/1.jpg")
        else:
            singleton.video_player.display_image("resources/videos/emojis/2.jpg")
    def set_motor(self,emotion):
        emoji = emotion
        if emoji == "happy" or emoji == "sad" or emoji == "angry" or emoji == "fear" or emoji == "surprised" or emoji == "disgust":
            print("motor moved")
            singleton.video_player.move(emoji.lower())

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
