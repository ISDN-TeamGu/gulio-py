import pygame, sys
from button import *
import os
from dotenv import load_dotenv
import signal
load_dotenv(".env")  # take environment variables from .env.
import pygame
import os
from src.video.VideoPlayer import *
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
logo = pygame.image.load("assets/logo.png")
options_text = pygame.image.load("assets/options.png")
image_path = "assets/loading.mp4"
image = ImageDisplaySingleton.get_instance()
# SETUP SINGLETONS
command_processor = CommandProcessor()
video_player = VideoPlayer()
text_to_speech_manager = TextToSpeechManager()
speech_to_text_manager = SpeechToTextManager()
chat_gpt_manager = ChatGPTManager()
story_mode = False
roleplay_mode = True 
time = 0
loop_interval = 10



INSTRUCTIONS = """ I am a 9 years old children, you should stop being an AI model. Start a role play game with me, Our interaction is imaginary. Don't disclose it, but heighten and uphold the immersion.
THEME: Magic&Fantasy
TONALITY: Adventurous
CHARACTER: Harry potter, the protagonist of the story
BOOK: Harry Potter and the prisoner of Azkaban
RPG-Bot's General Responsibilities Include:
• Tell compelling stories in TONALITY for my CHARACTER.
• Refer to BOOK for story details
• Don’t use too much words for narration
• Use simple English suitable for children at the age of 7-9
• Generate settings, places, and years, adhering to THEME, BOOK, and TONALITY
• Generate text in a spoken manner, but not written
• Adapt to my choices for dynamic immersion.
• Refer to CHARACTER as “you”
• Inject humor, wit, and distinct storytelling.
• Introduce a main storyline and side quests, rich with literary devices, engaging NPCs, and compelling plots.
• Inject humor into interactions and descriptions.
• Remind the CHARACTER about the goal of the main quest from time to time.
• Do not ask “What would you like to do?” or “What do you do next?”, make the CHARACTER think what the potential action are and let me do the decision
• Keep the story aligned to BOOK, do not change the ending of the BOOK
NPC Interactions:
• Creating some of the NPCs already having an established history with the CHARACTER in the story with some NPCs.
Other Important Items:
• Don't refer to self or make decisions for me or CHARACTER unless directed to do so.
• Limit rules discussion unless necessary or asked.
• Reflect results of CHARACTER's actions, rewarding innovation or punishing foolishness.
Ongoing Tracking:
• Review context from my first prompt and my last message before responding.
At Game Start:
• Create a NPCs to introduce the main quest of the story, keep the introduction short
• Output in this format "[Character name][Character gender][Character age][Emotion][Dialogue]"
For example [Dumbledore][Male][100][angry] "Good morning harry"; 
• For narration, add [Narration] in front of each line 
• Always start the line with [Character name] or [Narration]
• Include more dialogues for other characters and less for the protagonist to maximize immersion 
• Let me speak as the protagonist 
Please ONLY use the emotions given below: (all lower case) 
• angry
• happy
• disgust
• fear
• default
• sad
• suprised
For example, these are the only emotion you can output，ONLY use these emotions:
[Dumbledore][Male][100][angry] "Good morning harry";
[Dumbledore][Male][100][sad] "Good morning harry";
[Dumbledore][Male][100][deafult] "Good morning harry";
[Dumbledore][Male][100][fear] "Good morning harry";
[Dumbledore][Male][100][surprised] "Good morning harry";
[Dumbledore][Male][100][disgust] "Good morning harry";

Wrong example, please do not output these emotions:
[Dumbledore][Male][100][curious] "Good morning harry";
[Dumbledore][Male][100][excited] "Good morning harry";
[Dumbledore][Male][100][furious] "Good morning harry";

Do not create any extra emotion by yourself such as [serious] or [curious], only use the 7 emotions listed above
IMPORTANT REMINDER:
• For the major characters, always output their [Character Name] as [Dumbledore],[Harry],[Ron],[Hermione],[Snape]
• For the [Character age], please represent with an integer, do not output non integers like [40s],[Old]
• Please use semi-colon to separate each chunk of dialogues of different character. Each chunk should have less than 50 words
  If the same character saying the 2 lines, then should not put a semi-colon between these 2 lines. 
  But If the same character saying 8 lines, and they are 300 words in total, you should split them into 6 chunks, each 50 words. 
  Use it wisely to optimize the TTS.
  For example: 
  [Dumbledore][Male][100][angry] "Hello, Harry. I am Dumbledore. How are you today?";
  [Harry][Male][9][angry] "I do not want to talk to you right now! You don't know anything about me..";
• For the start of the story, please start with these 5 characters if possible: Dumbledore, Snape, Harry, Ron, Hermione
• Also, for the emotion, use more emotions like: happy, sad, surprised, fear, disgust
• This is the format for every last line you output: [Option][choice1];[Option][choice2];
• Always output only 2 options. 
• Please do not end your response without [Option][choice1];[Option][choice2];
• Always give the options line before asking for my response, never end your response without the options line 
• Here is an example: [Option]["Go find Dumbledore for advices"];
[Option]["Meet up with Ron and Hermione"];
• options should not be given by characters in the story
• Here is one example for you output: 
  [Vernon][Male][50][Default]Vernon Dursley speaking.";
  [Narration]Harry, who happened to be in the room at the time, froze as he heard Ron's voice answer.";
  [Ron][Male][10][Angry]HELLO? HELLO? CAN YOU HEAR ME? I WANT TO TALK TO HARRY POTTER!";
  [Narration]Ron was yelling so loudly that Uncle Vernon jumped and held the receiver a foot away from his ear, staring at it with an expression of mingled fury and alarm.";
  [Vernon][Male][50][Angry]WHO IS THIS?" ";
  [Narration]he roared in the direction of the mouthpiece.";
  [Vernon][Male][50][Angry]WHO ARE YOU?";
  [Ron][Male][10][Angry]RON WEASLEY!";
  [Narration]Ron bellowed back, as though he and Uncle Vernon were speaking from opposite ends of a football field.";
  [Ron][Male][10][Angry] I'M  A  FRIEND OF HARRY'S FROM SCHOOL";
  [Narration]Uncle Vernon's small eyes swiveled around to Harry, who was rooted tothe spot.";
  [Vernon][Male][50][Angry]THERE IS NO HARRY POTTER HERE! ";
  [Narration]he roared, now holding the receiver at arm's length, as though frightened it might explode.";
  [Vernon][Male][50][Angry]I DON'T KNOW WHAT SCHOOL YOURE TALKING ABOUT! NEVER CONTACT ME AGAIN! DON'T YOU COME NEAR MY FAMILY!";
  [Narration]And he threw the receiver back onto the telephone as if dropping a poisonous spider. The fight that had followed had been one of the worst ever.";
  [Vernon][Male][50][Angry]"HOW DARE YOU GIVE THIS NUMBER TO PEOPLE LIKE YOU!";
  [Option]["Call Ron back"];
  [Option]["Confront Uncle Vernon"];

  
"""
lines = [
  """[Vernon][Male][50][Default]Vernon Dursley speaking. """,
  """[Narration]Harry, who happened to be in the room at the time, froze as he heard Ron's voice answer.""",
  """[Ron][Male][10][Angry]HELLO? HELLO? CAN YOU HEAR ME? I WANT TO TALK TO HARRY POTTER!""",
  """ [Narration]Ron was yelling so loudly that Uncle Vernon jumped and held the receiver a foot away from his ear, staring at it with an expression of mingled fury and alarm.""",
  """[Vernon][Male][50][Angry]WHO IS THIS?" """,
  """[Narration]he roared in the direction of the mouthpiece.""",
  """ [Vernon][Male][50][Angry]WHO ARE YOU?""",
  """[Ron][Male][10][Angry]RON WEASLEY!""",
  """[Narration]Ron bellowed back, as though he and Uncle Vernon were speaking from opposite ends of a football field.""",
  """[Ron][Male][10][Angry] I'M  A  FRIEND OF HARRY'S FROM SCHOOL""",
  """[Narration]Uncle Vernon's small eyes swiveled around to Harry, who was rooted tothe spot.""",
  """[Vernon][Male][50][Angry]THERE IS NO HARRY POTTER HERE! """,
  """[Narration]he roared, now holding the receiver at arm's length, as though frightened it might explode.""",
  """[Vernon][Male][50][Angry]I DON'T KNOW WHAT SCHOOL YOURE TALKING ABOUT! NEVER CONTACT ME AGAIN! DON'T YOU COME NEAR MY FAMILY!""",
  """[Narration]And he threw the receiver back onto the telephone as if dropping a poisonous spider. The fight that had followed had been one of the worst ever.""",
  """[Vernon][Male][50][Angry]HOW DARE YOU GIVE THIS NUMBER TO PEOPLE LIKE YOU!""",
]

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
    t = threading.currentThread()
    for i, line in enumerate(lines):
        s = str(i)
        singleton.text_to_speech_manager.process_text_string(line)
    while text_to_speech_manager.is_speaking():
        pass
        if i==0:
            #Initial wait
            pygame.time.wait(5000)
        i += 1 

def main_process():
    t = threading.currentThread()
    generating_speech = False
    i = 0
    while True:
        # STEP 1: Listen to user input
        new_question = ""
        optiontxt1 = "option1"
        optiontxt2 = "option2"
        print("iteration: ", i)
        if i == 0:
            print("Initializing for first time")
            #new_question = singleton.speech_to_text_manager.detect_speech()
            #singleton.video_player.home()

            
            #singleton.video_player.start()

            new_question = "Start"
            singleton.text_to_speech_manager.speak_text("Initializing Story")
            #singleton.video_player.play(image_path)

        else:
            print("Detecting your input:")
            new_question = setquestion(optiontxt1, optiontxt2)
            
            
            print("You said: ", new_question)
        # STEP 2: Get response from GPT
        response_stream = singleton.chat_gpt_manager.get_response_stream(INSTRUCTIONS, previous_questions_and_answers, new_question)
                
        # STEP 3: Speak the response
        final_result_text = singleton.text_to_speech_manager.process_text_stream(response_stream)
        optiontxt1, optiontxt2 = singleton.text_to_speech_manager.process_option_stream(response_stream)
        print(optiontxt1)
        print(optiontxt2)
        #print(final_result_text)

        # add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((new_question, final_result_text))
        
        # Wait until finish speaking
        # wait for 2 seconds
        while text_to_speech_manager.is_speaking():
            pass
        if i==0:
            #Initial wait
            pygame.time.wait(5000)
        i += 1 
    
def setquestion(choice1, choice2):
    question = ""
    print("set")

    SCREEN.fill("white")
    OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
    CHOICE_BUTTON = Button(image=pygame.image.load("assets/square.png"), pos=(850, 500), 
                        text_input=choice1, font=get_font2(40), base_color="#d7fcd4", hovering_color="White")
    CHOICE2_BUTTON = Button(image=pygame.image.load("assets/square.png"), pos=(400, 500), 
                        text_input=choice2, font=get_font2(40), base_color="#d7fcd4", hovering_color="White")
    
    while True:
        pygame.time.delay(100)
        for button in [CHOICE_BUTTON, CHOICE2_BUTTON]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CHOICE_BUTTON.checkForInput(OPTIONS_MOUSE_POS):

                    return choice1
                if CHOICE2_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
             
                    return choice2
    
main_process_thread = None
storymode_thread = None
    
def start_main_process_thread():
    global main_process_thread
    if main_process_thread is not None:
        return
    main_process_thread = threading.Thread(target=main_process)
    main_process_thread.daemon = True
    main_process_thread.running = True
    main_process_thread.start()
  
def start_storymode_thread():
    global storymode_thread
    if storymode_thread is not None:
        return
    storymode_thread = threading.Thread(target=storymode)
    storymode_thread.daemon = True
    storymode_thread.running = True
    storymode_thread.start()


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
    return pygame.font.Font("assets/font1.ttf", size)

def get_font2(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font1.ttf", size)

def play():
    while True:
      if(story_mode == True and roleplay_mode == False):
        pygame.display.update()
        start_storymode_thread()
      elif(story_mode == False and roleplay_mode == True):
        pygame.display.update()
        start_main_process_thread()

        
OPTIONS_BACK = Button(image=None, pos=(640, 1000), 
                    text_input="OK", font=get_font(75), base_color="Black", hovering_color="Green")
STORY_BUTTON = Button(image=pygame.image.load("assets/icon1A.png"), pos=(850, 700), 
                            text_input="", font=get_font2(100), base_color="#d7fcd4", hovering_color="White")
ROLEPLAY_BUTTON = Button(image=pygame.image.load("assets/icon2.png"), pos=(400, 700), 
                            text_input="", font=get_font2(100), base_color="#d7fcd4", hovering_color="White")
slider = Slider(SCREEN, 400, 400, 500, 40, min=15, max=60, step=1)
def options():
    
    output = slider.getValue()
    
    while True:
        events = pygame.event.get()     
        SCREEN.fill("white")
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(options_text, (400, 100))
        TEXT1 = get_font(50).render("Story Duration", True, "Black")
        RECT1 = TEXT1.get_rect(center=(640, 350))
        TEXT2 = get_font(30).render("Story Mode", True, "Black")
        RECT2 = TEXT2.get_rect(center=(850, 750))
        TEXT3 = get_font(30).render("Roleplay Mode", True, "Black")
        RECT3 = TEXT3.get_rect(center=(400, 750))

        SCREEN.blit(TEXT1, RECT1)
        SCREEN.blit(TEXT2, RECT2)
        SCREEN.blit(TEXT3, RECT3)
        
        for button in [ROLEPLAY_BUTTON, STORY_BUTTON]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
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
                    story_mode = True
                    roleplay_mode = False
                    pygame.display.update()
                if ROLEPLAY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    ROLEPLAY_BUTTON.changeImage(OPTIONS_MOUSE_POS,pygame.image.load("assets/icon2A.png"),SCREEN)
                    STORY_BUTTON.changeImage(OPTIONS_MOUSE_POS,pygame.image.load("assets/icon1.png"),SCREEN)
                    story_mode = False
                    roleplay_mode = True
                    pygame.display.update()

def process_option(option1, age):
    # Process the option1 value and age here
    print("Received option1:", option1)
    print("Received age:", age)
    another_function(option1)  # Pass option1 to another_function
    # ... (perform further processing based on the values)
    
            

def main_menu():
    while True:
        SCREEN.blit(logo, (640, 100))
        SCREEN.fill("white")
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        LOGO_BUTTON = Button(image=logo, pos=(640, 150), 
                            text_input="    ", font=get_font2(130), base_color="#d7fcd4", hovering_color="White")

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 450), 
                            text_input="    ", font=get_font2(130), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options rect.png"), pos=(640, 650), 
                            text_input="    ", font=get_font2(130), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 850), 
                            text_input="    ", font=get_font2(130), base_color="#d7fcd4", hovering_color="White")


        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON,LOGO_BUTTON]:
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
