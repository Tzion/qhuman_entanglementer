import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from leds_experiments import run_effects
from config import SPEECH_PATH
from audio_manager import AudioPlayer
from time import sleep
import random

def play_audio_once_in_while():
    while True:
        audio_player = AudioPlayer()
        print('playing sound')
        audio_player.play_sound('../media/speech/explain_short_hebrew.mp3')
        sleep_time_minutes = random.randint(1, 3)
        sleep_time_seconds = sleep_time_minutes * 60
        print(f'sleeping for {sleep_time_minutes} minutes')
        sleep(sleep_time_seconds)

if __name__ == "__main__":
    play_audio_once_in_while()
