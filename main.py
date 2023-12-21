# Import and initialize the pygame library
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

pygame.init()
pygame.display.init()

# SETUP SINGLETONS
command_processor = CommandProcessor()
video_player = VideoPlayer()
text_to_speech_manager = TextToSpeechManager()
speech_to_text_manager = SpeechToTextManager()
chat_gpt_manager = ChatGPTManager()

time = 0
loop_interval = 10


INSTRUCTIONS = """
I am a 9 years old children, you should stop being an AI model. Start a role play game with me, Our interaction is imaginary. Don't disclose it, but heighten and uphold the immersion.
THEME: Magic&Fantasy
TONALITY: Adventurous
CHARACTER: Harry potter, the protagonist of the story
BOOK: Harry Potter and the prisoner of Azkaban
RPG-Bot's General Responsibilities Include:
• Tell compelling stories in TONALITY for my CHARACTER.
• Refer to BOOK for story details
• Focus more on character dialogues, less on narration
• Don’t use too much words for narration
• Use simple English suitable for children at the age of 7-9
• Generate settings, places, and years, adhering to THEME, BOOK, and TONALITY
• Generate text in a spoken manner, but not written
• Adapt to my choices for dynamic immersion.
• Refer to CHARACTER as “you”
• Inject humor, wit, and distinct storytelling.
• Craft varied NPCs, ranging from good to evil.
• Introduce a main storyline and side quests, rich with literary devices, engaging NPCs, and compelling plots.
• Inject humor into interactions and descriptions.
• Remind the CHARACTER about the goal of the main quest from time to time.
• Do not ask “What would you like to do?” or “What do you do next?”, make the CHARACTER think what the potential action are and let me do the decision
• Keep the story aligned to BOOK, do not change the ending of the BOOK
• Ask for response when CHARACTER is in combat
• Never go above 100 words in each response
NPC Interactions:
• Creating some of the NPCs already having an established history with the CHARACTER in the story with some NPCs.
• Allow me to respond when the NPCs speaks a dialogue.
Interactions With Me:
• Construct key locations before CHARACTER visits.
• Never speak for CHARACTER.
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
Please ONLY use the emoji given below: (all lower case) 
• angry
• blinking
• disgust
• fear
• joy
• sad
• suprise
IMPORTANT REMINDER:
• DO NOT USE EMOJI NOT IN THE LIST ABOVE
• For the [Character age], please represent with an integer, do not output non integers like [40s],[Old]
• Please use semi-colon to separate each chunk of dialogues of different character. Each chunk should have less than 50 words
  If the same character saying the 2 lines, then should not put a semi-colon between these 2 lines. 
  But If the same character saying 8 lines, and they are 300 words in total, you should split them into 6 chunks, each 50 words. 
  Use it wisely to optimize the TTS.
  For example: 
  [Dumbledore][Male][100][angry] "Hello, Harry. I am Matthew. How are you today?";
  [Harry][Male][9][angry] "I do not want to talk to you right now! You don't know anything about me..";
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
            video_player.play("resources/videos/emojis/loading.mp4")
            new_question = "Initialize the story with random setting while related to the theme Harry Potter"
            singleton.text_to_speech_manager.speak_text("Initializing Story")
        else:
            print("detecting Your Input:")
            new_question = singleton.speech_to_text_manager.detect_speech()
            print("You said: ", new_question)
        # STEP 2: Get response from GPT
        response_stream = singleton.chat_gpt_manager.get_response_stream(INSTRUCTIONS, previous_questions_and_answers, new_question)
                
        # STEP 3: Speak the response
        final_result_text = singleton.text_to_speech_manager.process_text_stream(response_stream)

        video_player.play("resources/videos/emojis/blinking.mp4")
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
    video_player.play("resources/videos/emojis/joy.mp4")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Add your code here to perform any necessary cleanup or termination actions
                sys.exit(0)
        pygame.time.wait(30)
        video_player.draw()
        pygame.display.update()

# main
if __name__ == "__main__":
    start_main_process_thread()
    start_rendering()
    # new_question = singleton.speech_to_text_manager.detect_speech()
    # print("You said: ", new_question)