
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

        
class TextToSpeechManager:
    def __init__(self):
        singleton.text_to_speech_manager = self

    #Function to split the output to multiple line for calling voice acting separately 
    def process_text(self, text):
        lines = [line.strip() for line in text.split("\n")]
        for key in lines:
            self.run_dialogue_with_attribute(key)
            
    #Obtain the attributes like age or name from output to customize voice acting 
    def run_dialogue_with_attribute(self, line):
        
        try:
            substrings = []
            in_brackets = False
            current_substring = ""
            dialogue = ""
            
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
                self.voice(gender,age,emotion,dialogue)
            if name != "Narration":
                gender = substrings[1]
                age = substrings[2]
                emotion = substrings[3]
                print("with emoji: "+emotion)
                singleton.video_player.play("resources/videos/emojis/"+emotion.lower()+".mp4")
                self.voice(gender,age,emotion,dialogue)
        except:
            print("Error in parsing the output")
            pass

    #Function to call voice acting API
    def voice(self, gender,age,emotion,dialogue):
        singleton.command_processor.play_emoji(emotion)
        if gender == "Narration":
            asyncio.run(AIvoice.async_main(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[dialogue],quality="faster",interactive=False,use_async=True,voice="s3://mockingbird-prod/abigail_vo_6661b91f-4012-44e3-ad12-589fbdee9948/voices/speaker/manifest.json"))
        elif gender == "Male":
            if int(age) > 40:
                asyncio.run(AIvoice.async_main(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[dialogue],quality="faster",interactive=False,use_async=True,voice="s3://mockingbird-prod/hook_1_chico_a3e5e83f-08ae-4a9f-825c-7e48d32d2fd8/voices/speaker/manifest.json"))
            else:
                asyncio.run(AIvoice.async_main(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[dialogue],quality="faster",interactive=False,use_async=True,voice="s3://peregrine-voices/nolan saad parrot/manifest.json"))
        elif gender == "Female":   
            if int(age) > 40:
                asyncio.run(AIvoice.async_main(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[dialogue],quality="faster",interactive=False,use_async=True,voice="s3://voice-cloning-zero-shot/7c38b588-14e8-42b9-bacd-e03d1d673c3c/nicole/manifest.json"))
            else: 
                asyncio.run(AIvoice.async_main(user="Wip26iViI4fvUgFHjj9oaIFQjWA2",key=os.getenv("PLAYHT_API_KEY"),text=[dialogue],quality="faster",interactive=False,use_async=True,voice="s3://peregrine-voices/donna_parrot_saad/manifest.json"))



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