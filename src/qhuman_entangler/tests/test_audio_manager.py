import unittest
import pygame
from qhuman_entangler.audio_manager import BaseAudioPlayer

class TestAudioPlayers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.mixer.init()

    def setUp(self):
        self.audio_player: BaseAudioPlayer = BaseAudioPlayer()

    def test_play_sound(self):
        sound_file = "media/sound/test.mp3"
        self.audio_player.play_sound(sound_file)

    def test_play_speech(self):
        text = "I am the Quantum Entangler, prepare to be entangled"
        self.audio_player.play_speech(text)

    def tearDown(self):
        self.audio_player.stop()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

if __name__ == "__main__":
    unittest.main()
