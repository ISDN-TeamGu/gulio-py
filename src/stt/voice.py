import os
import sounddevice as sd
from google.cloud import speech_v1p1beta1 as speech

def transcribe_streaming():
    client = speech.SpeechClient()

    # Configure the speech recognition request
    language_code = "en-US"
    config = {
        "encoding": speech.RecognitionConfig.AudioEncoding.LINEAR16,
        "sample_rate_hertz": 16000,
        "language_code": language_code,
    }
    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)

    # Start streaming audio from the microphone
    with sd.InputStream(callback=process_microphone_chunk):
        print("Listening... (Press Ctrl+C to stop)")
        while True:
            pass

def process_microphone_chunk(indata, frames, time, status):
    # Process the microphone audio chunk
    if status:
        print("Error:", status)
    else:
        audio_chunk = indata.tobytes()

        # Send the streaming request with the audio chunk
        response = client.streaming_recognize(
            streaming_config,
            requests=[
                speech.StreamingRecognizeRequest(audio_content=audio_chunk)
            ]
        )

        # Process the streaming response
        for result in response.results:
            if result.is_final:
                text = result.alternatives[0].transcript
                print("Final transcription:", text)
            else:
                text = result.alternatives[0].transcript
                print("Interim transcription:", text)

# Call the function to perform real-time streaming transcription with live audio input
transcribe_streaming()