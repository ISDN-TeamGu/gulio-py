import os
import openai
from test import *
import numpy as np
import asyncio
#import simpleaudio as sa
from speech import *
import threading
from playsound import playsound
openai.api_key = "9baa7f75e05c4b29925a5a738d4c7b0d" #apikey
openai.api_base = "https://isdn4001.openai.azure.com/"
openai.api_type = 'azure'
openai.api_version = '2023-05-15' 

deployment_name='ISDN4001' 

INSTRUCTIONS = """
I am a 7 years old children, you should stop being an AI model. Start a role play game with me, Our interaction is imaginary. Don't disclose it, but heighten and uphold the immersion.
THEME: Fantasy&Fun
TONALITY: Adventurous
CHARACTER: Charlie and the chocolate factory, the protagonist of the story
BOOK: Charlie and the chocolate factory
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
• Do not ask “What would you like to do?” or “What do you do next?”, 
make the CHARACTER think what the potential action are and let me do the decision
• Keep the story aligned to BOOK, do not change the ending of the BOOK
• Ask for response when CHARACTER is in combat
• Never go above 100 words in each response
• Include more dialogues for other characters and less for the protagonist to maximize immersion 
• Let me speak as the protagonist 
NPC Interactions:
• Creating some of the NPCs already having an established 
history with the CHARACTER in the story with some NPCs.
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
• For the [Character age], please represent with an integer, do not ouput non integers like [40s],[Old]
For example "[Willy wonka][Male][40][Happy] "Good morning Charlie" "
• For narration, add [Narration] in front of each line 
• Always start the line with [Character name] or [Narration]
• Please only split line when the character who speaks the dialogue is changed, 
for dialogue spoken by the same character, please keep it written in the same line
•There are 2 types of soundeffects in this story, footsteps and door open sound, when character in the story open a door or move location, indicate using a soundeffect by outputting a single 
line of text like this "[Soundeffect][Footsteps]" or "[Soundeffect][Door]", please use this two format only, do not include soundeffect other than door and footsteps, use [Soundeffect] only, do not use 
anything like [SFX],[Sound]. 
•Do not output in format like [SFX][Door] in any circumstance 
"""

TEMPERATURE = 0.5
MAX_TOKENS = 1000
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
sound1 = AudioSegment.from_wav("soundeffects/door.wav")
sound2 = AudioSegment.from_wav("soundeffects/Footsteps.wav")
# limits how many questions we include in the prompt
MAX_CONTEXT_QUESTIONS = 100

def listToString(s):
 
    # initialize an empty string
    str1 = " "
 
    # return string
    for ele in s:
        str1 += ele
 
    # return string
    return str1

#Function to split the output to multiple line for calling voice acting separately 
def splitLine(text):
    lines = [line.strip() for line in text.split("\n")]
    for key in lines:
        get_attribute(key)
        
#Obtain the attributes like age or name from output to customize voice acting 
def get_attribute(line):
    
 
    substrings = []
    in_brackets = False
    current_substring = ""
    dialogue = ""
    name=""
    for c in line:
        if c == "[":
            in_brackets = True
        elif c == "]" and in_brackets:
            substrings.append(current_substring)
            current_substring = ""
            in_brackets = False
        elif in_brackets:
            current_substring += c
        elif in_brackets == False:
            dialogue += c
    if current_substring:
        substrings.append(current_substring)
    name = substrings[0]
    
        
    if name == "Narration":
        gender = "Narration"
        age = "Narration"
        emotion = "Narration"
        voice(gender,age,emotion,dialogue)
    elif name=="":
        gender = "Narration"
        age = "Narration"
        emotion = "Narration"
        voice(gender,age,emotion,dialogue)
    if name == "Soundeffect" :
        if substrings[1] == "Footsteps":
            sfx(substrings[1])
            
        elif substrings[1] == "Door":
            sfx(substrings[1])     
    if name != "Narration" and name != "Soundeffect":
        gender = substrings[1]
        age = substrings[2]
        emotion = substrings[3]
        voice(gender,age,emotion,dialogue)
    
        
def play_sound(file):
    playsound(file)
def sfx(effect):
    if (effect == "Door"):
        sound_thread = threading.Thread(target=play_sound, args=("soundeffects/door.wav",))
        sound_thread.start()
    elif (effect == "Footsteps"):
        sound_thread = threading.Thread(target=play_sound, args=("soundeffects/Footsteps.wav",))
        sound_thread.start()
#Function to call voice acting API
def voice(gender,age,emotion,dialogue):
    if gender == "Narration":
        asyncio.run(AIvoice.async_main(user="Wip26iViI4fvUgFHjj9oaIFQjWA2 ",key="9c3ad5651e494eae91108f4fa0041c77",text=[dialogue],quality="faster",interactive=False,use_async=True,voice="s3://mockingbird-prod/abigail_vo_6661b91f-4012-44e3-ad12-589fbdee9948/voices/speaker/manifest.json"))
    elif gender == "Male":
        if int(age) > 30:
            asyncio.run(AIvoice.async_main(user="Wip26iViI4fvUgFHjj9oaIFQjWA2 ",key="9c3ad5651e494eae91108f4fa0041c77",text=[dialogue],quality="faster",interactive=False,use_async=True,voice="s3://mockingbird-prod/hook_1_chico_a3e5e83f-08ae-4a9f-825c-7e48d32d2fd8/voices/speaker/manifest.json"))
        else:
            asyncio.run(AIvoice.async_main(user="Wip26iViI4fvUgFHjj9oaIFQjWA2 ",key="9c3ad5651e494eae91108f4fa0041c77",text=[dialogue],quality="faster",interactive=False,use_async=True,voice="s3://peregrine-voices/nolan saad parrot/manifest.json"))
    elif gender == "Female":   
        if int(age) > 30:
            asyncio.run(AIvoice.async_main(user="Wip26iViI4fvUgFHjj9oaIFQjWA2 ",key="9c3ad5651e494eae91108f4fa0041c77",text=[dialogue],quality="faster",interactive=False,use_async=True,voice="s3://voice-cloning-zero-shot/7c38b588-14e8-42b9-bacd-e03d1d673c3c/nicole/manifest.json"))
        else: 
            asyncio.run(AIvoice.async_main(user="Wip26iViI4fvUgFHjj9oaIFQjWA2 ",key="9c3ad5651e494eae91108f4fa0041c77",text=[dialogue],quality="faster",interactive=False,use_async=True,voice="s3://peregrine-voices/donna_parrot_saad/manifest.json"))

#Function to call openAI API
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
    splitLine(completion.choices[0].message.content.replace('\n\n', '\n'))


    return completion.choices[0].message.content
#def ask_gpt(prompt):
	#response = openai.Completion.create(engine=deployment_name, prompt=prompt, max_tokens=1000)
	#message = response.choices[0].text.strip()
	#print(message)

#def story(prompt):
	#ask_gpt(prompt)
	#while True:
		#user_input = input("You: ")
		#if user_input.lower() == "exit":
			#print("ChatGPT: Goodbye!")
			#break 	
		#response = ask_gpt(user_input)
		#print("ChatGPT:", response)
#text = response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()

#main function
previous_questions_and_answers = []
while True:
    new_question = input()
    response = get_response(INSTRUCTIONS, previous_questions_and_answers, new_question)
    if new_question.lower() == "exit":
	    print("ChatGPT: Goodbye!")
	    break 	
	# add the new question and answer to the list of previous questions and answers
    previous_questions_and_answers.append((new_question, response))