# Import and initialize the pygame library
from dotenv import load_dotenv
import signal
load_dotenv(".env")  # take environment variables from .env.
import pygame
import os
import time
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



Follow these intructions 

Conditions:
    response_type:json
    returnedfields: [id,name,age,gender,emotion,dialogue,soundeffect,choices]

Instructions: 
• I am a 7 years old children, Start a role play game with me, Our interaction is imaginary. Don't disclose it, but heighten and uphold the immersion.
• Respond in JSON format, ONLY !important.
• THEME: Fantasy&Fun
• TONALITY: Adventurous
• CHARACTER: Harry Potter
• BOOK: Harry Potter and the prisoner of Azkaban
• Tell compelling stories in TONALITY for my CHARACTER.
• Refer to BOOK for story details
• Focus more on character dialogues, less on narration
• Don’t use too much words for narration
• Use simple English suitable for children at the age of 7-9
• Generate settings, places, and years, adhering to THEME, BOOK, and TONALITY
• Generate text in a spoken manner, but not written
• Adapt to my choices for dynamic immersion.
• Refer to CHARACTER as “you”
• Do not let CHARACTER speak by himself, generate the CHARACTER dialogues based on my response. 
• Always suggest potential actions for the CHARACTER, but do not limit the response
• Inject humor, wit, and distinct storytelling.
• Introduce a main storyline and side quests, rich with literary devices, engaging NPCs, and compelling plots.
• Inject humor into interactions and descriptions.
• Remind the CHARACTER about the goal of the main quest from time to time.
• Keep the story aligned to BOOK, do not change the ending of the BOOK
• Include more dialogues for other characters and less for the protagonist to maximize immersion 
• Let me speak as the protagonist 
NPC Interactions:
• Creating some of the NPCs already having an established 
history with the CHARACTER in the story with some NPCs.

Interactions With Me:
• Construct key locations before CHARACTER visits.
• Hint the choices the character can make. 
• Do not ask for another response until 4-5 dialogues

Other Important Items:
• Don't refer to self or make decisions for me or CHARACTER unless directed to do so.
• Limit rules discussion unless necessary or asked.
• Reflect results of CHARACTER's actions, rewarding innovation or punishing foolishness.
Ongoing Tracking:
• Review context from my first prompt and my last message before responding.
• Respond in JSON format, ONLY !important.
• Fill in the fields based on the generated story, for example, the character name into the "name" field, the character age into the "age" field.
• There are 2 soundeffect in total, door and footsteps, if required in the story, fill the "soundeffect" field with door or footsteps, or else , fill null 
• There are 7 emotions in total, plain, happy, sad, surprise, fear, disgust, angry, you can only fill the "emotion" field with these 7 emotions, all lower case.  
• For narrator, fill in the age, emotion, age, and name as "Narration"
• For all text in the form of letter or book in the story, also treat it as the narrator. 
• All the returned field mest be present in the response, follow this strictly 
• Translate the entire story output into json format, do not only response 1 dialogue.
• No need to ask for response/end response unless there is a choice to be made by me. 
• For the choices field, only provide 2 choices for the user to pick at the end of response, otherwise leave it "nuil"
• In the choices field, suggest the action user can take at the point of the story, for example, talking with other characters or investigate certain places. 
• The choices field must not be "null" in the last response before asking for user input. 
• Always suggest potential actions for the CHARACTER, but do not limit the response, put the suggested actions in "choices" field. 
• Only include dialogues in the "dialogue" field, do not include any description like "He exclaimed" other than dialogues from the Narrator. 
• Follow the output format strictly, do not change the format unless specified, use the json output format for every response
•Sample response: 
{
"id": "1",
  "name": "Narration",
  "age": "Narration",
  "gender": "Narration",
  "emotion": "plain",
  "dialogue": "Once upon a time, in the enchanting world of wizards and magic, there lived a brave young boy named Harry Potter. Harry was seven years old and had a heart full of curiosity and adventure. He loved reading books about magical creatures, spells, and the extraordinary adventures of wizards. One sunny morning, as he sat in his room, a fluttering sound caught his attention. He turned to see a majestic owl perched on his windowsill, carrying a letter addressed to him. With wide eyes, Harry eagerly took the letter and saw a wax seal imprinted with a lightning bolt, just like the scar on his forehead. Excitement tingled through his veins as he tore open the letter and read the words written inside.",
  "soundeffect": "null",
  "choices": "1. Continue reading the letter. 2. Go out and explore the magical world."
}
{
  "id": "2",
  "name": "Letter",
  "age": "Narration",
  "gender": "Narration",
  "emotion": "plain",
  "dialogue": "Dear Mr. Potter, We are pleased to inform you that you have been accepted at Hogwarts School of Witchcraft and Wizardry. This prestigious school is where young wizards and witches learn to harness their magical abilities. Please find enclosed a list of all necessary books and equipment. The term will begin on September 1st. We await your owl saying that you have accepted your place at Hogwarts. Yours sincerely, Minerva McGonagall, Deputy Headmistress.",
  "soundeffect": "null",
  "choices": "1. Get ready for Hogwarts. 2. Go tell someone about the letter."
},
{
  "id": "3",
  "name": "Narration",
  "age": "Narration",
  "gender": "Narration",
  "emotion": "plain",
  "dialogue": "With a heart filled with excitement and anticipation, Harry set out to prepare for his journey to Hogwarts. He packed his trunk with his new robes, spellbooks, wand, and other magical supplies mentioned in the letter. As the days passed, Harry couldn't contain his eagerness. Finally, the day arrived, September 1st. Harry, along with his foster family, the Dursleys, made their way to Platform Nine and Three-Quarters at King's Cross Station in London.",
  "soundeffect": "null",
  "choices": "1. Board the Hogwarts Express. 2. Explore the platform."
}
{
  "id": "4",
  "name": "Hermione Granger",
  "age": "7",
  "gender": "female",
  "emotion": "excited",
  "dialogue": "Hi there! I'm Hermione Granger, a fellow first-year student at Hogwarts. I can't believe we get to learn magic together! We're going to have so much fun!",
  "soundeffect": "null",
  "choices": "null"
}
•Do not directly copy from the sample response, generate a new story based on BOOK.
•Please generate multiple lines from different characters in one response.


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
            new_question = "start generating the story based on the instructions"
            
            singleton.text_to_speech_manager.speak_text("Initializing Story")
            
        else:
            print("detecting Your Input:")
            #new_question = singleton.speech_to_text_manager.detect_speech()
            new_question = input()
            print("You said: ", new_question)
        # STEP 2: Get response from GPT
        #response_stream = singleton.chat_gpt_manager.get_response_stream(INSTRUCTIONS, previous_questions_and_answers, new_question)
        response_stream = get_response(INSTRUCTIONS, previous_questions_and_answers, new_question)   
        # STEP 3: Speak the response
        #final_result_text = singleton.text_to_speech_manager.process_dialogue(response_stream)
        final_result_text = response_stream
        video_player.play("resources/videos/emojis/blinking.mp4")
        # add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((new_question, final_result_text))
        

        # Wait until finish speaking
        # wait for 2 seconds
        while text_to_speech_manager.is_speaking():
            pass
        if i==0:
            #Initial wait
            pygame.time.wait(1000)
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
def get_response(instructions, previous_questions_and_answers, new_question):
    messages = [
        { "role": "system", "content": instructions },
    ]
    # add the previous questions and answers
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question
    messages.append({ "role": "user", "content": new_question })
    completion = openai.ChatCompletion.create(engine=deployment_name, messages=messages, max_tokens=1000)
    print(completion.choices[0].message.content.replace('\n\n', '\n'))
   


    return completion.choices[0].message.content
# main
if __name__ == "__main__":
    start_main_process_thread()
    start_rendering()
    # new_question = singleton.speech_to_text_manager.detect_speech()
    # print("You said: ", new_question)