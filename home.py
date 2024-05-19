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
[Narration]”Harry Potter was a highly unusual boy in many ways. For one thing, he
hated the summer holidays more than any other time of year. For another,
he really wanted to do his homework but was forced to do it in secret,
in the dead of night. And he also happened to be a wizard.
It was nearly midnight, and he was lying on his stomach in bed, the
blankets drawn right over his head like a tent, a flashlight in one hand
and a large leather-bound book propped open against the pillow. Harry moved the tip of his
eagle-feather quill down the page, frowning as he looked for something
that would help him write his essay, "Witch Burning in the Fourteenth
Century Was Completely Pointless discuss."
The quill paused at the top of a likely-looking paragraph. Harry Pushed
his round glasses up the bridge of his nose, moved his flashlight closer
to the book, and read:
Non-magic people (more commonly known as Muggles) were particularly
afraid of magic in medieval times, but not very good at recognizing it.
On the rare occasion that they did catch a real witch or wizard, burning
had no effect whatsoever. The witch or wizard would perform a basic
Flame Freezing Charm and then pretend to shriek with pain while enjoying
a gentle, tickling sensation. Indeed, Wendelin the Weird enjoyed being
burned so much that she allowed herself to be caught no less than
fortyseven times in various disguises.
Harry put his quill between his teeth and reached underneath his pillow
for his ink bottle and a roll of parchment. Slowly and very carefully he
unscrewed the ink bottle, dipped his quill into it, and began to write,
pausing every now and then to listen, because if any of the Dursleys
heard the scratching of his quill on their way to the bathroom, he'd
probably find himself locked in the cupboard under the stairs for the
rest of the summer.
The Dursley family of number four, Privet Drive, was the reason that
Harry never enjoyed his summer holidays. Uncle Vernon, Aunt Petunia, and
their son, Dudley, were Harry's only living relatives. They were
Muggles, and they had a very medieval attitude toward magic. Harry's
dead parents, who had been a witch and wizard themselves, were never
mentioned under the Dursleys' roof For years, Aunt Petunia and Uncle
Vernon had hoped that if they kept Harry as downtrodden as possible,
they would be able to squash the magic out of him. To their fury, they
had been unsuccessful. These days they lived in terror of anyone finding
out that Harry had spent most of the last two years at Hogwarts School
of Witchcraft and Wizardry. The most they could do, however, was to lock
away Harry's spellbooks, wand, cauldron, and broomstick at the start of
the summer break, and forbid him to talk to the neighbors.
This separation from his spellbooks had been a real problem for Harry,
because his teachers at Hogwarts had given him a lot of holiday work.
One of the essays, a particularly nasty one about shrinking potions, was
for Harry's least favorite teacher, Professor Snape, who would be
delighted to have an excuse to give Harry detention for a month. Harry
had therefore seized his chance in the first week of the holidays. While
Uncle Vernon, Aunt Petunia, and Dudley had gone out into the front
garden to admire Uncle Vernon's new company car (in very loud voices, so
that the rest of the street would notice it too), Harry had crept
downstairs, picked the lock on the cupboard under the stairs, grabbed
some of his books, and hidden them in his bedroom. As long as he didn't
leave spots of ink on the sheets, the Dursleys need never know that he
was studying magic by night.
Harry was particularly keen to avoid trouble with his aunt and uncle at
the moment, as they were already in an especially bad mood with him, all
because he'd received a telephone call from a fellow wizard one week
into the school vacation.
Ron Weasley, who was one of Harry's best friends at Hogwarts, came from
a whole family of wizards. This meant that he knew a lot of things Harry
didn't, but had never used a telephone before. Most unluckily, it had
been Uncle Vernon who had answered the call.”

[Vernon][Male][50][Default]"Vernon Dursley speaking."
[Narration]”Harry, who happened to be in the room at the time, froze as he heard
Ron's voice answer.”

[Ron][Male][10][Angry]"HELLO? HELLO? CAN YOU HEAR ME? I WANT TO TALK TO
HARRY POTTER!"
[Narration]”Ron was yelling so loudly that Uncle Vernon jumped and held the receiver
a foot away from his ear, staring at it with an expression of mingled
fury and alarm.”
[Vernon][Male][50[Angry]"WHO IS THIS?" 

[Narration]”he roared in the direction of the mouthpiece.” 

[Vernon][Male][50[Angry]"WHO ARE YOU?" 

[Ron][Male][10][Angry]"RON WEASLEY!" 

[Narration]”Ron bellowed back, as though he and Uncle Vernon were
speaking from opposite ends of a football field.”

[Ron][Male][10][Angry] "I'M  A  FRIEND OF HARRY'S FROM SCHOOL"
[Narration]”Uncle Vernon's small eyes swiveled around to Harry, who was rooted to
the spot.”
[Vernon][Male][50[Angry]"THERE IS NO HARRY POTTER HERE!" 

[Narration]”he roared, now holding the receiver at arm's length, as though frightened it might explode.”

[Vernon][Male][50[Angry]"I DON'T KNOW WHAT SCHOOL YOURE TALKING ABOUT! NEVER CONTACT ME AGAIN! DON'T YOU COME NEAR MY FAMILY!"
[Narration]”And he threw the receiver back onto the telephone as if dropping a
poisonous spider. The fight that had followed had been one of the worst ever.”
[Vernon][Male][50[Angry]"HOW DARE YOU GIVE THIS NUMBER TO PEOPLE LIKE PEOPLE LIKE
YOU!"
"""

INSTRUCTIONS = """
I am a 9 years old children, you should stop being an AI model. Tell a story for me, Follow strictly the dialogues from the BOOK I provided.

BOOK: Harry Potter and the prisoner of Azkaban
Story-Bot's General Responsibilities Include:
• Refer to BOOK for story details
• Keep the story aligned to BOOK, do not change the ending of the BOOK
• Change the original dialogues from the BOOK into our format disclosed below 
Other Important Items:
• Limit rules discussion unless necessary or asked.
Ongoing Tracking:
At Game Start:
• Output in this format "[Character name][Character gender][Character age][Emotion][Dialogue]"
For example [Dumbledore][Male][100][angry] "Good morning harry"; 
• For narration, add [Narration] in front of each line 
• Always start the line with [Character name] or [Narration]
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
"""


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
def main_process():
    t = threading.currentThread()
    generating_speech = False
    i = 0
    while True:
        # STEP 1: Listen to user input
        new_question = ""
        print("iteration: ", i)
        if i == 0:
            print("Initializing for first time")
            #new_question = singleton.speech_to_text_manager.detect_speech()
            #singleton.video_player.draw_button()
            singleton.video_player.display_image(image_path)
            #singleton.video_player.start()

            new_question = "Initialize the story with random setting while related to the theme Harry Potter"
            singleton.text_to_speech_manager.speak_text("And so the story begins")
        else:
            print("detecting Your Input:")
            new_question = "continue"
            print("You said: ", new_question)
        # STEP 2: Get response from GPT
        #response_stream = singleton.chat_gpt_manager.get_response_stream(INSTRUCTIONS, previous_questions_and_answers, new_question)
                
        # STEP 3: Speak the response
        #final_result_text = singleton.text_to_speech_manager.process_text_stream(response_stream)
        final_result_text = singleton.text_to_speech_manager.process_text_string(STORY)
        singleton.video_player.display_image(image_path)
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
