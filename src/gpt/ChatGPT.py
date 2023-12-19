import os
import openai
import numpy as np
import asyncio
import simpleaudio as sa
from src.stt.SpeechToText import *
import src.singleton as singleton

openai.api_key = os.getenv("OPENAI_API_KEY") #apikey
openai.api_base = "https://isdn4001.openai.azure.com/"
openai.api_type = 'azure'
openai.api_version = '2023-05-15' 

deployment_name='ISDN4001'


TEMPERATURE = 0.5
MAX_TOKENS = 1000
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
# limits how many questions we include in the prompt
MAX_CONTEXT_QUESTIONS = 100

class ChatGPTManager:
    def __init__(self):
        singleton.chat_gpt_manager = self
    #Function to call openAI API
    def get_response(self, instructions, previous_questions_and_answers, new_question):
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
        return completion.choices[0].message.content.replace('\n\n', '\n')


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
