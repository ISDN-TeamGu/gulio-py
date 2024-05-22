import speech_recognition as sr


r = sr.Recognizer()
speech = sr.Microphone(device_index=1)
with speech as source:
    audio = r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
try:
    recog = r.recognize_google(audio, language = 'en-US')
    print("You said: " + recog)
except:
    print("error")
