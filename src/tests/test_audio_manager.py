import unittest
import pygame
from audio_players import RaspberryPiAudioPlayer, ComputerAudioPlayer

class TestAudioPlayers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.mixer.init()

    def setUp(self):
        self.raspberry_pi_player = RaspberryPiAudioPlayer()
        self.computer_player = ComputerAudioPlayer()

    def test_play_sound(self):
        # Test playing a sound (replace with actual sound file)
        sound_file = "sound.wav"
        self.raspberry_pi_player.play_sound(sound_file)
        self.computer_player.play_sound(sound_file)
        # Add assertions for checking if the sound plays as expected

    def test_play_speech(self):
        # Test playing speech
        text = "This is a test of speech synthesis."
        self.raspberry_pi_player.play_speech(text)
        self.computer_player.play_speech(text)
        # Add assertions for checking if speech plays as expected

    def tearDown(self):
        self.raspberry_pi_player.stop()
        self.computer_player.stop()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

if __name__ == "__main__":
    unittest.main()
