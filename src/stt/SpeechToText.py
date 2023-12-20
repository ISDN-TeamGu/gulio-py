import argparse

from pvcheetah import CheetahActivationLimitError, create
from pvrecorder import PvRecorder
import os
import src.singleton as singleton
# from pydub import AudioSegment
# from pydub.playback import play


class SpeechToTextManager:
    def __init__(self):
        self.processRate = 1.0
        singleton.speech_to_text_manager = self
        self.setup()
    def setup(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--access_key',
            help='AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)')
        parser.add_argument(
            '--library_path',
            help='Absolute path to dynamic library. Default: using the library provided by `pvcheetah`')
        parser.add_argument(
            '--model_path',
            help='Absolute path to Cheetah model. Default: using the model provided by `pvcheetah`')
        parser.add_argument(
            '--endpoint_duration_sec',
            type=float,
            default=1,
            help='Duration in seconds for speechless audio to be considered an endpoint')
        parser.add_argument(
            '--disable_automatic_punctuation',
            action='store_true',
            help='Disable insertion of automatic punctuation')
        parser.add_argument('--audio_device_index', type=int, default=-1, help='Index of input audio device')
        parser.add_argument('--show_audio_devices', action='store_true', help='Only list available devices and exit')
        args = parser.parse_args()

        if args.show_audio_devices:
            for index, name in enumerate(PvRecorder.get_available_devices()):
                print('Device #%d: %s' % (index, name))
            return


        self.cheetah = create(
            access_key=os.getenv("PVCHEETAH_API_KEY"),
            library_path=args.library_path,
            model_path=args.model_path,
            endpoint_duration_sec=args.endpoint_duration_sec,
            enable_automatic_punctuation=not args.disable_automatic_punctuation)
        self.recorder = PvRecorder(frame_length=self.cheetah.frame_length, device_index=args.audio_device_index)

    def detect_speech(self):
        try:
            # sound1 = AudioSegment.from_wav("soundeffects/start.wav")
            # sound2 = AudioSegment.from_wav("soundeffects/stop.wav")
            print('Cheetah version : %s' % self.cheetah.version)

            self.recorder.start()
            print('Listening... (press Ctrl+C to stop)')
            result = ""
            try:
                passed = False
                # play(sound1)
                while True:
                    partial_transcript, is_endpoint, c_char_p= self.cheetah.process(self.recorder.read())
                    print(partial_transcript, end='', flush=True)
                    if c_char_p != '':
                        passed = True
                    if is_endpoint:
                        if passed == True:
                            self.recorder.stop()
                            # play(sound2)
                            return(self.cheetah.flush())
            finally:
                self.recorder.stop()
                return result

        except KeyboardInterrupt:
            pass
        except CheetahActivationLimitError:
            print('AccessKey has reached its processing limit.')


