import speech_recognition as sr
import pyttsx3
import threading

class SpeechService:
    def __init__(self):
        pass

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                return text
            except sr.WaitTimeoutError:
                return "No speech detected"
            except sr.UnknownValueError:
                return "Could not understand audio"
            except sr.RequestError:
                return "Could not request results"