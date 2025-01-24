import os
import azure.cognitiveservices.speech as speechsdk



class Speech_To_Text:
    def __init__(self):
        self.speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
        self.speech_config.speech_recognition_language="en-US"
        self.audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=self.audio_config)        

    def recognize_from_microphone(self):
        speech_recognition_result = self.speech_recognizer.recognize_once_async().get()
        return speech_recognition_result
    