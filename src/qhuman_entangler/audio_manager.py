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
        pygame.time.wait(int(sound.get_length() * 1000))  # Wait for the sound to finish


    def play_speech(self, text: str):
        tts = gTTS(text)
        try:
            tts.save("speech.mp3")
            self.play_sound("speech.mp3")
        finally:
            os.remove("speech.mp3")

    def stop(self):
        pygame.mixer.stop()

class RaspberryPiAudioPlayer(BaseAudioPlayer):
    pass

class ComputerAudioPlayer(BaseAudioPlayer):
    pass
