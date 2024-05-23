
from __future__ import annotations
import os
import openai
import numpy as np
import asyncio
import simpleaudio as sa
from src.stt.SpeechToText import *
import src.singleton as singleton
from typing import AsyncGenerator, AsyncIterable, Generator, Iterable, Literal
from src.motor.servoc import *
import time
import threading
import select
import sys



from pyht.client import Client, TTSOptions
from pyht.async_client import AsyncClient
from pyht.protos import api_pb2

openai.api_key = os.getenv("OPENAI_API_KEY") #apikey
openai.api_base = "https://isdn4001.openai.azure.com/"
openai.api_type = 'azure'
openai.api_version = '2023-05-15' 

deployment_name='ISDN4001'

video_lock = threading.Lock()
TEMPERATURE = 0.5
MAX_TOKENS = 1000
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
# limits how many questions we include in the prompt
MAX_CONTEXT_QUESTIONS = 100
option = False
def listToString(s):
 
    # initialize an empty string
    str1 = " "
 
    # return string
    for ele in s:
        str1 += ele
 
    # return string
    return str1

class SpeakTask:
    def __init__(self, dialogue, speech_attribute):
        self.dialogue = dialogue
        self.speech_attribute = speech_attribute
        self.preloaded = False
        self.is_done = False
        self.audio_stream = None
    def start_preloading(self, semaphore: threading.Semaphore):
        preload_thread = threading.Thread(target=self.preload, args=[semaphore])
        preload_thread.daemon = True
        preload_thread.start()
    def preload(self, semaphore: threading.Semaphore):
        semaphore.acquire()
        print("Start preloading audio: ", self.dialogue)
        if self.speech_attribute["name"] == "options":
            option = True
            self.audio_stream = asyncio.run(preload_playht(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=["Harry, how will you act? Here are your choices"+""+self.dialogue],quality="faster",interactive=False,use_async=True,voice="s3://mockingbird-prod/abigail_vo_6661b91f-4012-44e3-ad12-589fbdee9948/voices/speaker/manifest.json"))
            singleton.video_player.home("option1","option2")
        elif self.speech_attribute["gender"] == "Narration":
            self.audio_stream = asyncio.run(preload_playht(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[self.dialogue],quality="faster",interactive=False,use_async=True,voice="s3://mockingbird-prod/abigail_vo_6661b91f-4012-44e3-ad12-589fbdee9948/voices/speaker/manifest.json"))
        elif self.speech_attribute["gender"] == "Male":
            if self.speech_attribute["name"] == "Harry":
                self.audio_stream = asyncio.run(preload_playht(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[self.dialogue],quality="faster",interactive=False,use_async=True,voice="s3://voice-cloning-zero-shot/2b4d2337-497c-4d51-b9b5-48034a546b77/original/manifest.json"))
            elif self.speech_attribute["name"] == "Ron":
                self.audio_stream = asyncio.run(preload_playht(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[self.dialogue],quality="faster",interactive=False,use_async=True,voice="s3://voice-cloning-zero-shot/9d4801d5-90a1-44b8-bed3-b8efeca2659f/original/manifest.json"))
            elif self.speech_attribute["name"] == "Snape":
                self.audio_stream = asyncio.run(preload_playht(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[self.dialogue],quality="faster",interactive=False,use_async=True,voice="s3://voice-cloning-zero-shot/186331e7-4ecb-4cac-9bc5-8ab3052827c0/original/manifest.json"))
            elif self.speech_attribute["name"] == "Dumbledore":
                self.audio_stream = asyncio.run(preload_playht(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[self.dialogue],quality="faster",interactive=False,use_async=True,voice="s3://voice-cloning-zero-shot/9c974caf-d50f-4c34-aa6f-6ed49697c81a/original/manifest.json"))
            elif int(self.speech_attribute["age"]) > 40:
                self.audio_stream = asyncio.run(preload_playht(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[self.dialogue],quality="faster",interactive=False,use_async=True,voice="s3://mockingbird-prod/hook_1_chico_a3e5e83f-08ae-4a9f-825c-7e48d32d2fd8/voices/speaker/manifest.json"))
            else:
                self.audio_stream = asyncio.run(preload_playht(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[self.dialogue],quality="faster",interactive=False,use_async=True,voice="s3://peregrine-voices/nolan saad parrot/manifest.json"))
        elif self.speech_attribute["gender"] == "Female":   
            if self.speech_attribute["name"] == "Hermione":
                self.audio_stream = asyncio.run(preload_playht(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[self.dialogue],quality="faster",interactive=False,use_async=True,voice="s3://voice-cloning-zero-shot/03e2546e-a7c9-45b7-9b24-050a0ecf027d/original/manifest.json"))
            elif int(self.speech_attribute["age"]) > 40:
                self.audio_stream = asyncio.run(preload_playht(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[self.dialogue],quality="faster",interactive=False,use_async=True,voice="s3://voice-cloning-zero-shot/7c38b588-14e8-42b9-bacd-e03d1d673c3c/nicole/manifest.json"))
            else: 
                self.audio_stream = asyncio.run(preload_playht(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[self.dialogue],quality="faster",interactive=False,use_async=True,voice="s3://peregrine-voices/donna_parrot_saad/manifest.json"))
        #Predict preload finish or not
        asyncio.run(asyncio.sleep(2+0.05 * len(self.dialogue)))
        print("delaying: ", 0.05 * len(self.dialogue))
        print("Finished preloaded audio: ", self.dialogue)
        self.preloaded = True
        semaphore.release()
    
    async def play(self):

        print("Playing SpeakTask: ", self.dialogue, self.speech_attribute)
        singleton.command_processor.play_emoji(self.speech_attribute["name"].lower(),self.speech_attribute["emotion"].lower())
       
        singleton.command_processor.set_motor(self.speech_attribute["emotion"])
        if self.audio_stream is not None:
            print("audio_stream: ", self.audio_stream)
            
            await asyncio.wait_for(async_play_audio(self.audio_stream), 60)
            self.audio_stream.close()
            self.audio_stream = None
            self.is_done = True
            
            print("Speak task is done!", self.is_done)
            

class TextToSpeechManager:
    def __init__(self):
        singleton.text_to_speech_manager = self
        self.current_speech_attribute = {
            "name": "Narration",
            "gender": "Female",
            "age": "35",
            "emotion": "blinking"
        }
        # Multithreading
        self.lock = threading.Lock()
        self.tasks = []
        self.current_task = None
        self.playing_thread = None
        self.semaphore = threading.Semaphore(3)  # Limiting preloads to 3 at same time


    def process_text_stream(self, stream):
        temp = ""
        sentences = []
        option = False
        for chunk in stream:
            content = chunk["choices"][0].get("delta", {}).get("content") 
            if content is not None:
                temp += content
            # when detected full stop, question mark, exclamation mark, comma or new line, process the text
            if(";" in temp or "!" in temp or "?" in temp or "\n" in temp):
                # print("sentence: ", temp)
                # If the text detected flag like [Narration] or [Character name], update current attribute
                dialogue = self.process_dialogue(temp)
                sentences.append(dialogue)
                # Process text
                self.speak_text(dialogue)
                #print(dialogue)
                temp = ""
        
        # Make result
        return "".join(sentences)
    def process_text_string(self, text_string):
        
        dialogue = self.process_dialogue(text_string)
               
     
        self.speak_text(dialogue)
                
    
      

   
        
        
    # Obtain the attributes like age or name from output to customize voice acting 
    def process_dialogue(self, line):
        try:
            
            substrings = ["Narrator", "Narration", "35", "blinking", "", "" ,"" ,""]
            load_attribute = False
            in_brackets = False
            current_substring = ""
            dialogue = ""
            
            argIndex = 0
            for c in line:
                if c == "[":
                    in_brackets = True
                    load_attribute = True
                elif c == "]" and in_brackets:
                    substrings[argIndex] = current_substring
                    argIndex += 1
                    current_substring = ""
                    in_brackets = False
                elif in_brackets:
                    current_substring += c
                elif in_brackets == False:
                    dialogue += c
            if current_substring:
                substrings[argIndex] = current_substring
                argIndex += 1
            
            # Load the attributes
            if load_attribute:
                print(substrings)
                self.current_speech_attribute["name"] = substrings[0]
                if (self.current_speech_attribute["name"]=="options"):
                    option = True 
                    dialogue = substrings[1]
                else:
                     self.current_speech_attribute["gender"] = substrings[1]
                     try:
                         self.current_speech_attribute["age"] = int(substrings[2])
                     except:
                         pass
                     self.current_speech_attribute["emotion"] = substrings[3]
                     if self.current_speech_attribute["emotion"] != "happy" and self.current_speech_attribute["emotion"] != "default" and self.current_speech_attribute["emotion"] != "sad" and self.current_speech_attribute["emotion"] != "fear" and self.current_speech_attribute["emotion"] != "disgust" and self.current_speech_attribute["emotion"] != "surprised":
                         self.current_speech_attribute["emotion"] = "default"
                
                # print("Loaded speech attribute: ", self.current_speech_attribute)
            return dialogue
        except Exception as e:
            print("Error in parsing the output", e)
        return ""

    # Add the speak task according to text
    def speak_text(self, text):
        # print("speak_text: ", text)
        if(text is None):
            return
        if(text == ""):
            return
        lines = [line.strip() for line in text.split("\n")]
        for line in lines:
            self.add_speak_task(line, self.current_speech_attribute.copy())
            # print("speak text task: ", line, self.current_speech_attribute)

    
    # Multithreading
    def add_speak_task(self, dialogue, speech_attribute):
        if(dialogue is None):
            return
        if(len(dialogue) < 2):
            return
        speak_task = SpeakTask(dialogue, speech_attribute)
        speak_task.start_preloading(self.semaphore)
        self.tasks.append(speak_task)
        return speak_task
    def play_current_task(self):
        if self.current_task is not None:
            asyncio.run(self.current_task.play())
    def play_next_task(self):
        # get the first task in tasks
        if len(self.tasks) > 0:
            self.current_task = self.tasks.pop(0)
            while self.current_task.audio_stream == None:
                time.sleep(0.1)
            self.playing_thread = threading.Thread(target=self.play_current_task)
            self.playing_thread.daemon = True
            self.playing_thread.start()

    def try_next_task(self):
        if self.current_task == None:
            self.play_next_task()
            return
        if self.current_task.is_done:
            self.play_next_task()
            return

    
    def check_tasks(self):
        while True:
            with self.lock:
                self.try_next_task()
                time.sleep(0.1)
    def is_speaking(self):
        if  len(self.tasks) > 0:
            return True
        if self.playing_thread is not None:
            return self.playing_thread.is_alive()

    def start(self):
        check_thread = threading.Thread(target=self.check_tasks)
        check_thread.daemon = True
        check_thread.start()

    


async def preload_playht(
    user: str,
    key: str,
    text: Iterable[str],
    voice: str,
    quality: Literal["fast"] | Literal["faster"],
    interactive: bool,
    use_async: bool,
):  
    del use_async

    # Setup the client
    client = AsyncClient(user, key)

    # Set the speech options
    options = TTSOptions(voice=voice, format=api_pb2.FORMAT_WAV, quality=quality)

# Get the streams
    in_stream, out_stream = client.get_stream_pair(options)

# Send text, play audio.
    await in_stream(*text)
    await in_stream.done()
      
# Cleanup.
    await client.close()
    return out_stream



async def async_play_audio(data: AsyncGenerator[bytes, None] | AsyncIterable[bytes]):
    buff_size = 10485760
    ptr = 0
    start_time = time.time()
    buffer = np.empty(buff_size, np.float16)
    audio = None
    i = -1
    async for chunk in data:
        i += 1
        if i == 0:
            start_time = time.time()
            continue  # Drop the first response.
        elif i == 1:
            print("First audio byte received in:", time.time() - start_time)
        for sample in np.frombuffer(chunk, np.float16):
            buffer[ptr] = sample
            ptr += 1
        if i == 5:
        # Give a 4 sample worth of breathing room before starting
        # playback
            audio = sa.play_buffer(buffer, 1, 2, 24000)
    approx_run_time = ptr / 24_000
    await asyncio.sleep(max(approx_run_time - time.time() + start_time, 0))
    if audio is not None:
        time.sleep(1)
        audio.stop() 
