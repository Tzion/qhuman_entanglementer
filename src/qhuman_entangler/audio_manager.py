import pygame
from gtts import gTTS
import os
import io
import logging
import random
import requests
from typing import Tuple

log = logging.getLogger(__name__)

media_powerup = "media/powerup/"
media_speech = "media/speech/"
media_entanglement = "media/entanglement/"



class AudioPlayerInterface:
    def play_sound(self, file_path: str):
        pass
    
    def play_text(self, text: str):
        pass

    def stop(self):
        pass

    def pause(self):
        pass

class AudioPlayer(AudioPlayerInterface):
    def __init__(self):
        log.info('Initializing audio player')
        pygame.init()
        self.mixer = pygame.mixer
        self.mixer.init()
        self.init_sound_tracks()

    def init_sound_tracks(self):
        self.sound_tracks = {}
        for folder in [media_powerup, media_speech, media_entanglement]:
            log.debug(f'initialize tracks inside folder: {folder}')
            audio_files = [file for file in os.listdir(folder) if file.endswith(('.mp3', '.wav', '.ogg'))]
            self.sound_tracks[folder] = [(file, self.mixer.Sound(folder + file)) for file in audio_files]

    def pick_track(self, folder) -> Tuple[str, pygame.mixer.Sound]:
        tracks = self.sound_tracks[folder]
        return random.choice(tracks)


    def play_powerup(self):
        track = self.pick_track(media_powerup)
        self.play_sound(track)

    def play_entanglement_with_leds(self):
        self.stop() # stop any playing sound
        track = self.pick_track(media_entanglement)
        duration_ms = track[1].get_length() * 1000
        try:
            response = requests.get(f'http://localhost:5000/entanglement?duration_ms={duration_ms}', timeout=4)
        except requests.exceptions.RequestException as e:
            log.error('Error while sending entanglement request to led server: %s', e)
        log.debug('Response from led server: %s', response)
        self.play_sound(track, wait_till_done=False)

    def play_explain(self):
        self.stop()
        track = self.pick_track(media_speech)
        self.play_sound(track, wait_till_done=False)

    def play_sound(self, track: Tuple[str, pygame.mixer.Sound],  wait_till_done=False):
        name, sound = track
        log.info('Playing sound: %s', name)
        sound.play()
        if wait_till_done:
            pygame.time.wait(int(sound.get_length() * 1000))  # Wait for the sound to finish


    def play_text(self, text: str):
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
