import pygame
from gtts import gTTS
import os
import io

class AudioPlayerInterface:
    def play_sound(self, name: str):
        pass
    
    def play_speech(self, text: str):
        pass

    def stop(self):
        pass

class BaseAudioPlayer(AudioPlayerInterface):
    def __init__(self):
        pygame.init()
        self.mixer = pygame.mixer
        self.mixer.init()

    def play_sound(self, name: str):
        sound = pygame.mixer.Sound(name)
        sound.play()

    def play_speech(self, text: str):
        tts = gTTS(text)
        audio_data = io.BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)
        sound = pygame.mixer.Sound(buffer=audio_data.read())
        sound.play()

    def stop(self):
        pygame.mixer.stop()

class RaspberryPiAudioPlayer(BaseAudioPlayer):
    pass

class ComputerAudioPlayer(BaseAudioPlayer):
    pass
