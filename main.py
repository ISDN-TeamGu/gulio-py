# Import and initialize the pygame library
from dotenv import load_dotenv
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
os.environ["DISPLAY"] = ":0"
pygame.display.init()

# SETUP SINGLETONS
command_processor = CommandProcessor()
video_player = VideoPlayer()
text_to_speech_manager = TextToSpeechManager()
speech_to_text_manager = SpeechToTextManager()
chat_gpt_manager = ChatGPTManager()

time = 0
loop_interval = 10

# video_player.play("resources/videos/emojis/joy.mp4")


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
For example "[Dumbledore][Male][100][angry] "Good morning harry" "
• For narration, add [Narration] in front of each line 
• Always start the line with [Character name] or [Narration]
• Include more dialogues for other characters and less for the protagonist to maximize immersion 
• Let me speak as the protagonist 
Possible emotion list: (all lower case)
• angry
• blinking
• disgust
• fear
• joy
• sad
• suprise


• Joy
• Sad
Blinking

"""


# User Input Command
def command_prompt():
    while True:
        response = input('Please enter the command: ')
        command_processor.run_command(response)


command_prompt_thread = threading.Thread(target=command_prompt)
command_prompt_thread.start()


# Main Process
previous_questions_and_answers = []
def main_process():
    while True:
        print("detecting Your Input:")
        # STEP 1: Listen to user input
        new_question = singleton.speech_to_text_manager.detect_speech()
        print("You said: ", new_question)
        
        # STEP 2: Get response from GPT
        response = singleton.chat_gpt_manager.get_response(INSTRUCTIONS, previous_questions_and_answers, new_question)


        if new_question.lower() == "exit":
            print("ChatGPT: Goodbye!")
            break 	

        
        # STEP 3: Speak the response
        singleton.text_to_speech_manager.process_text(response)


        # add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((new_question, response))

main_process_thread = threading.Thread(target=main_process)
# main_process_thread.start()


# Drawing Display
while True:
    pygame.time.wait(30)
    video_player.window.fill((  0,255,  0))
    pygame.display.update()
    # video_player.draw()

