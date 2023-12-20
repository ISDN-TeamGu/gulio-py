
from __future__ import annotations
import os
import openai
import numpy as np
import asyncio
import simpleaudio as sa
from src.stt.SpeechToText import *
import src.singleton as singleton
from typing import AsyncGenerator, AsyncIterable, Generator, Iterable, Literal

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


TEMPERATURE = 0.5
MAX_TOKENS = 1000
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
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

class SpeakTask:
    def __init__(self, dialogue, speech_attribute):
        self.dialogue = dialogue
        self.speech_attribute = speech_attribute
        self.is_done = False
    def play(self):
        print("Playing SpeakTask: ", self.dialogue)
        
        if self.speech_attribute["gender"] == "Narration":
            asyncio.run(AIvoice.async_main(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[self.dialogue],quality="faster",interactive=False,use_async=True,voice="s3://mockingbird-prod/abigail_vo_6661b91f-4012-44e3-ad12-589fbdee9948/voices/speaker/manifest.json"))
        elif self.speech_attribute["gender"] == "Male":
            if int(self.speech_attribute["age"]) > 40:
                asyncio.run(AIvoice.async_main(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[self.dialogue],quality="faster",interactive=False,use_async=True,voice="s3://mockingbird-prod/hook_1_chico_a3e5e83f-08ae-4a9f-825c-7e48d32d2fd8/voices/speaker/manifest.json"))
            else:
                asyncio.run(AIvoice.async_main(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[self.dialogue],quality="faster",interactive=False,use_async=True,voice="s3://peregrine-voices/nolan saad parrot/manifest.json"))
        elif self.speech_attribute["gender"] == "Female":   
            if int(self.speech_attribute["age"]) > 40:
                asyncio.run(AIvoice.async_main(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[self.dialogue],quality="faster",interactive=False,use_async=True,voice="s3://voice-cloning-zero-shot/7c38b588-14e8-42b9-bacd-e03d1d673c3c/nicole/manifest.json"))
            else: 
                asyncio.run(AIvoice.async_main(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[self.dialogue],quality="faster",interactive=False,use_async=True,voice="s3://peregrine-voices/donna_parrot_saad/manifest.json"))
            
        # When done
        self.is_done = True
        print("Speak task is done!")

class TextToSpeechManager:
    def __init__(self):
        singleton.text_to_speech_manager = self
        self.current_speech_attribute = {
            "name": "Narrator",
            "gender": "Male",
            "age": "35",
            "emotion": "Blinking"
        }
        # Multithreading
        self.lock = threading.Lock()
        self.tasks = []
        self.current_task_index = -1
        self.playing_thread = None


    def process_text_stream(self, stream):
        temp = ""
        sentences = []
        for chunk in stream:
            content = chunk["choices"][0].get("delta", {}).get("content") 
            if content is not None:
                temp += content
            # when detected full stop, question mark, exclamation mark, comma or new line, process the text
            if("." in temp or "?" in temp or "!" in temp or "\n" in temp):
                print("sentence: ", temp)
                # If the text detected flag like [Narration] or [Character name], update current attribute
                dialogue = self.process_dialogue(temp)
                sentences.append(dialogue)
                # Process text
                self.speak_text(dialogue)
                temp = ""
        
        # Make result
        return "".join(sentences)
        
            
    # Obtain the attributes like age or name from output to customize voice acting 
    def process_dialogue(self, line):
        try:
            
            substrings = ["Narrator", "Male", "35", "Blinking", "", "" ,"" ,""]
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
                self.current_speech_attribute["gender"] = substrings[1]
                self.current_speech_attribute["age"] = substrings[2]
                self.current_speech_attribute["emotion"] = substrings[3]
                print("Loaded speech attribute: ", self.current_speech_attribute)
            return dialogue
        except Exception as e:
            print("Error in parsing the output", e)
        return ""

    # Add the speak task according to text
    def speak_text(self, text):
        if(text is None):
            return
        if(text is ""):
            return
        lines = [line.strip() for line in text.split("\n")]
        for line in lines:
            self.add_speak_task(line, self.current_speech_attribute)
            print("speak text task: ", line)

    
    # Multithreading
    def add_speak_task(self, dialogue, speak_attribute):
        singleton.command_processor.play_emoji(speak_attribute["emotion"])
        speak_task = SpeakTask(dialogue, speak_attribute)
        self.tasks.append(speak_task)
        return speak_task

    def play_next_task(self):
        if self.current_task_index+1 < len(self.tasks):
            self.current_task_index += 1
            task = self.tasks[self.current_task_index]
            self.playing_thread = threading.Thread(target=task.play)
            self.playing_thread.start()
            self.playing_thread.join()
            self.play_next_task()
        else:
            self.current_task_index = -1
            self.playing_thread = None

    def play_tasks(self):
        if self.playing_thread is None or not self.playing_thread.is_alive():
            self.play_next_task()

    def check_tasks(self):
        while True:
            with self.lock:
                self.play_tasks()
            asyncio.wait(0.01)

    def start(self):
        check_thread = threading.Thread(target=self.check_tasks)
        check_thread.start()

class AIvoice:

    def main(
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
        client = Client(user, key)

    # Set the speech options
        options = TTSOptions(voice=voice, format=api_pb2.FORMAT_WAV, quality=quality)

    # Get the streams
        in_stream, out_stream = client.get_stream_pair(options)

    # Start a player thread.
        audio_thread = threading.Thread(None, play_audio, args=(out_stream,))
        audio_thread.start()

    # Send text, play audio.
        for t in text:
            in_stream(t)
        in_stream.done()

    # cleanup
        audio_thread.join()
        out_stream.close()

    # interactive session.
        if interactive:
            print("Starting interactive session.")
            print("Input an empty line to quit.")
            t = input("> ")
            while t:
                play_audio(client.tts(t, options))
                t = input("> ")
            print()
            print("Interactive session closed.")

    # Cleanup.
        client.close()
        return 0





    


    async def async_main(
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

        audio_task = asyncio.create_task(async_play_audio(out_stream))

    # Send text, play audio.
        await in_stream(*text)
        await in_stream.done()

    # cleanup
        await asyncio.wait_for(audio_task, 60)
        out_stream.close()

        async def get_input():
            while not select.select([sys.stdin], [], [], 0)[0]:
                await asyncio.sleep(0.01)
            return sys.stdin.readline().strip()

    #interactive session.
        if interactive:
            print("Starting interactive session.")
            print("Input an empty line to quit.")
            t = await get_input()
            while t:
                asyncio.ensure_future(async_play_audio(client.tts(t, options)))
                t = await get_input()
            print()
            print("Interactive session closed.")

    # Cleanup.
        await client.close()

        if __name__ == "__main__":
            import argparse

            parser = argparse.ArgumentParser("PyHT Streaming Demo")

            parser.add_argument(
                "--async", action="store_true", help="Use the asyncio client.", dest="use_async"
            )

            parser.add_argument(
                "--user", "-u", type=str, required=True, help="w67Bc740ToecfLroYCRQ2Dw042I3" ,
                default="w67Bc740ToecfLroYCRQ2Dw042I3",
            )
            parser.add_argument(
                "--key", "-k", type=str, required=True, help="7e684a86098e48359d38cc536e8b5769",
                default = "7e684a86098e48359d38cc536e8b5769",
            )
            parser.add_argument(
                "--voice",
                "-v",
                type=str,
                default="s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json",
                help="Voice manifest URI",
            )
            parser.add_argument(
                "--quality",
                "-q",
                choices=["fast", "faster"],
                default="faster",
                help="Quality of the generated audio",
            )

            input_group = parser.add_mutually_exclusive_group(required=True)
            input_group.add_argument(
                "--text",
                "-t",
                type=str,
                nargs="+",
                default=[],
                help="Text to generate, REQUIRED if the `--interactive` flag is not set.",
            )
            input_group.add_argument(
                "--interactive",
                "-i",
                action="store_true",
                help="Run this demo in interactive-input mode, REQUIRED if `--text` is not supplied.",
            )

            args = parser.parse_args()

            if args.use_async:
                asyncio.run(async_main(**vars(args)))
                sys.exit(0)

            sys.exit(main(**vars(args)))



def play_audio(data: Generator[bytes, None, None] | Iterable[bytes]):
    buff_size = 10485760
    ptr = 0
    start_time = time.time()
    buffer = np.empty(buff_size, np.float16)
    audio = None
    for i, chunk in enumerate(data):
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
    time.sleep(max(approx_run_time - time.time() + start_time, 0))
    if audio is not None:
        time.sleep(1)
        audio.stop()

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