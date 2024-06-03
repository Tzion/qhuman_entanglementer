import pygame
from audio_manager import AudioPlayer
from time import sleep
import random

def play_audio_once_in_while():
    while True:
        audio_player = AudioPlayer()
        audio_player.play_sound("media/speech/explain_short_hebrew.mp3")
        sleep_time = random.randint(10, 30)
        sleep_time_minutes = sleep_time * 60# * 60
        sleep(sleep_time_minutes)

if __name__ == "__main__":
    play_audio_once_in_while()