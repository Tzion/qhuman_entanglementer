import numpy as np
from pydub import AudioSegment
from pydub.playback import play

# Parameters
duration = 10.0  # in seconds
base_freq = 440.0  # in Hz
num_octaves = 1
sample_rate = 44100  # in Hz

# Generate a sine wave
def sine_wave(freq, duration, sample_rate, volume):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return 0.5 * np.sin(2 * np.pi * freq * t) * volume * t

# Generate a Shepard tone
def shepard_tone(base_freq, num_octaves, duration, sample_rate):
    tones = np.zeros(int(sample_rate * duration))
    max_freq = base_freq * (2 ** num_octaves)
    for i in range(num_octaves):
        freq = base_freq * (2 ** i)
        volume = freq / max_freq
        tones += sine_wave(freq, duration, sample_rate, volume)
    return tones

# Convert numpy array to audio
def numpy_to_audio(data, sample_rate):
    audio = (data * 32767).astype(np.int16)
    return AudioSegment(audio.tobytes(), frame_rate=sample_rate, sample_width=2, channels=1)

# Reverse audio
def reverse_audio(audio):
    return audio.reverse()

def main():
    # Create Shepard tone
    tone = shepard_tone(base_freq, num_octaves, duration, sample_rate)
    audio = numpy_to_audio(tone, sample_rate)

    # Play Shepard tone
    play(audio)

    # Reverse Shepard tone
    reversed_audio = reverse_audio(audio)

    # Play reversed Shepard tone
    play(reversed_audio)
