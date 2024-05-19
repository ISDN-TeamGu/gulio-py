import pygame, sys
from button import *
import os
from dotenv import load_dotenv
import signal
load_dotenv(".env")  # take environment variables from .env.
import pygame
import os
from src.video.VideoPlayer import VideoPlayer
from src.command.CommandProcessor import CommandProcessor
from multiprocessing import Process
import asyncio
import threading
import src.singleton as singleton
from src.tts.TextToSpeech import *
from src.stt.SpeechToText import *
from src.gpt.ChatGPT import *
from src.video.ImageDisplaySingleton import *
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from io import StringIO



pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
BG = pygame.image.load("assets/Background.jpg")

image_path = "resources/videos/emojis/1.jpg"
image = ImageDisplaySingleton.get_instance()
# SETUP SINGLETONS
command_processor = CommandProcessor()
video_player = VideoPlayer()
text_to_speech_manager = TextToSpeechManager()
speech_to_text_manager = SpeechToTextManager()
chat_gpt_manager = ChatGPTManager()

time = 0
loop_interval = 10

STORY = """
[Vernon][Male][50][Default]"Vernon Dursley speaking.";
[Narration]”Harry, who happened to be in the room at the time, froze as he heard Ron's voice answer.”;
[Ron][Male][10][Angry]"HELLO? HELLO? CAN YOU HEAR ME? I WANT TO TALK TO HARRY POTTER!";
[Narration]”Ron was yelling so loudly that Uncle Vernon jumped and held the receiver a foot away from his ear, staring at it with an expression of mingled fury and alarm.”;
[Vernon][Male][50[Angry]"WHO IS THIS?";
[Narration]”he roared in the direction of the mouthpiece.”;
[Vernon][Male][50[Angry]"WHO ARE YOU?"; 
[Ron][Male][10][Angry]"RON WEASLEY!"; 
[Narration]”Ron bellowed back, as though he and Uncle Vernon were speaking from opposite ends of a football field.”;
[Ron][Male][10][Angry] "I'M  A  FRIEND OF HARRY'S FROM SCHOOL";
[Narration]”Uncle Vernon's small eyes swiveled around to Harry, who was rooted tothe spot.”;
[Vernon][Male][50[Angry]"THERE IS NO HARRY POTTER HERE!"; 
[Narration]”he roared, now holding the receiver at arm's length, as though frightened it might explode.”;
[Vernon][Male][50[Angry]"I DON'T KNOW WHAT SCHOOL YOURE TALKING ABOUT! NEVER CONTACT ME AGAIN! DON'T YOU COME NEAR MY FAMILY!";
[Narration]”And he threw the receiver back onto the telephone as if dropping a poisonous spider. The fight that had followed had been one of the worst ever.”;
[Vernon][Male][50[Angry]"HOW DARE YOU GIVE THIS NUMBER TO PEOPLE LIKE YOU!";
"""

INSTRUCTIONS = """

"""
line1= """[Vernon][Male][50][Default]Vernon Dursley speaking. """
line2 = """[Narration]Harry, who happened to be in the room at the time, froze as he heard Ron's voice answer."""
line3 =  """[Ron][Male][10][Angry]HELLO? HELLO? CAN YOU HEAR ME? I WANT TO TALK TO HARRY POTTER!"""
line4 = """ [Narration]Ron was yelling so loudly that Uncle Vernon jumped and held the receiver a foot away from his ear, staring at it with an expression of mingled fury and alarm."""
line5 = """[Vernon][Male][50[Angry]WHO IS THIS?" """
line6 = """[Narration]he roared in the direction of the mouthpiece."""
line7 =""" [Vernon][Male][50[Angry]WHO ARE YOU?"""
line8 = """[Ron][Male][10][Angry]RON WEASLEY!"""
line9 = """[Narration]Ron bellowed back, as though he and Uncle Vernon were speaking from opposite ends of a football field."""
line10 = """[Ron][Male][10][Angry] I'M  A  FRIEND OF HARRY'S FROM SCHOOL"""
lien11 = """[Narration]Uncle Vernon's small eyes swiveled around to Harry, who was rooted tothe spot."""
line12 = """[Vernon][Male][50[Angry]THERE IS NO HARRY POTTER HERE! """
line13 = """[Narration]he roared, now holding the receiver at arm's length, as though frightened it might explode."""
line14 = """[Vernon][Male][50[Angry]I DON'T KNOW WHAT SCHOOL YOURE TALKING ABOUT! NEVER CONTACT ME AGAIN! DON'T YOU COME NEAR MY FAMILY!"""
line15 = """[Narration]And he threw the receiver back onto the telephone as if dropping a poisonous spider. The fight that had followed had been one of the worst ever."""
line16 = """[Vernon][Male][50[Angry]HOW DARE YOU GIVE THIS NUMBER TO PEOPLE LIKE YOU!"""
# User Input Command
def command_prompt():
    t = threading.currentThread()
    while getattr(t, "running", True):
        response = input('Please enter the command: ')
        command_processor.run_command(response)


command_prompt_thread = threading.Thread(target=command_prompt)
command_prompt_thread.daemon = True
command_prompt_thread.running = True
# command_prompt_thread.start()


# Main Process
previous_questions_and_answers = []
def storymode():
    
def main_process():
    singleton.text_to_speech_manager.process_text_string(line1)
    
    
main_process_thread = None
def start_main_process_thread():
    global main_process_thread
    if main_process_thread is not None:
        return
    main_process_thread = threading.Thread(target=main_process)
    main_process_thread.daemon = True
    main_process_thread.running = True
    main_process_thread.start()


# Speak Process
text_to_speech_manager.start()
# text_to_speech_manager.speak_text("Hello my friend")
# text_to_speech_manager.speak_text("This is a very long sentence, I am testing the text to speech function. And not only that.")
# text_to_speech_manager.speak_text("I have even tried to speak in a very fast speed. I am testing the text to speech function. And not only that.")
# text_to_speech_manager.speak_text("Thats why I am speaking in a very slow speed. I am helloing you all hahaha. And nobody knows.")


# Drawing Display
running = True

def signal_handler(sig, frame):
    running = False
    print('You pressed Ctrl+C!')
    print("quitted")
    command_prompt_thread.running = False
    main_process_thread.running = False
    pygame.quit()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def start_rendering():
    singleton.video_player.display_image(image_path)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Add your code here to perform any necessary cleanup or termination actions
                sys.exit(0)
        pygame.time.wait(30)
        #image.draw()
        video_player.draw()
        pygame.display.update()

# main
# if __name__ == "__main__":
#     start_main_process_thread()
#     start_rendering()
#     # new_question = singleton.speech_to_text_manager.detect_speech()
#     # print("You said: ", new_question)
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def get_font2(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font2.otf", size)

def play():
    while True:
        pygame.display.update()
        start_main_process_thread()
        
OPTIONS_BACK = Button(image=None, pos=(640, 1000), 
                    text_input="OK", font=get_font(75), base_color="Black", hovering_color="Green")
STORY_BUTTON = Button(image=pygame.image.load("assets/icon1.png"), pos=(850, 600), 
                            text_input="", font=get_font2(100), base_color="#d7fcd4", hovering_color="White")
ROLEPLAY_BUTTON = Button(image=pygame.image.load("assets/icon2.png"), pos=(400, 600), 
                            text_input="", font=get_font2(100), base_color="#d7fcd4", hovering_color="White")
slider = Slider(SCREEN, 200, 300, 800, 40, min=15, max=60, step=1)
def options():
    
    output = TextBox(SCREEN, 580, 370, 50, 50, fontSize=30)
    output.disable()  # Act as label instead of textbox
    
    while True:
        events = pygame.event.get()
        SCREEN.blit(BG, (0, 0))
    
     

        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_TEXT = get_font2(100).render("SETTINGS", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 80))
        TEXT1 = get_font(70).render("Story Duration", True, "Black")
        RECT1 = TEXT1.get_rect(center=(640, 250))
        TEXT2 = get_font(30).render("Story Mode", True, "Black")
        RECT2 = TEXT2.get_rect(center=(850, 750))
        TEXT3 = get_font(30).render("Roleplay Mode", True, "Black")
        RECT3 = TEXT3.get_rect(center=(400, 750))

        SCREEN.blit(TEXT1, RECT1)
        SCREEN.blit(TEXT2, RECT2)
        SCREEN.blit(TEXT3, RECT3)
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        for button in [ROLEPLAY_BUTTON, STORY_BUTTON]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        output.setText(slider.getValue())
        pygame_widgets.update(events)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        
                    main_menu()
                if STORY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    STORY_BUTTON.changeImage(OPTIONS_MOUSE_POS,pygame.image.load("assets/icon1A.png"),SCREEN)
                    ROLEPLAY_BUTTON.changeImage(OPTIONS_MOUSE_POS,pygame.image.load("assets/icon2.png"),SCREEN)
                    pygame.display.update()
                if ROLEPLAY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    ROLEPLAY_BUTTON.changeImage(OPTIONS_MOUSE_POS,pygame.image.load("assets/icon2A.png"),SCREEN)
                    STORY_BUTTON.changeImage(OPTIONS_MOUSE_POS,pygame.image.load("assets/icon1.png"),SCREEN)
                    pygame.display.update()

        

            

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font2(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font2(130), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 550), 
                            text_input="OPTIONS", font=get_font2(130), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 850), 
                            text_input="QUIT", font=get_font2(130), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
# User Input Command
