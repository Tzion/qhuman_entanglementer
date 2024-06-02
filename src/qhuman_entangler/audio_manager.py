import pygame
from gtts import gTTS
import os
import io
import logging

log = logging.getLogger(__name__)


class AudioPlayerInterface:
    def play_sound(self, name: str):
        pass
    
    def play_speech(self, text: str):
        pass

    def stop(self):
        pass

    def pasuse(self):
        pass

class AudioPlayer(AudioPlayerInterface):
    def __init__(self):
        pygame.init()
        self.mixer = pygame.mixer
        self.mixer.init()

    def play_sound(self, name: str):
        log.info('Playing sound: %s', name)
        sound = pygame.mixer.Sound(name)
        sound.play()
        # pygame.time.wait(int(sound.get_length() * 1000))  # Wait for the sound to finish


    def play_speech(self, text: str):
        tts = gTTS(text)
        try:
            tts.save("speech.mp3")
            self.play_sound("speech.mp3")
        finally:
            os.remove("speech.mp3")

    def pause(self):
        log.info('Pausing player',)
        pygame.mixer.pause()

    def stop(self):
        pygame.mixer.stop()

class RaspberryPiAudioPlayer(AudioPlayer):
    pass

class ComputerAudioPlayer(AudioPlayer):
    pass
