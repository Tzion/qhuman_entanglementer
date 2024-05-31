import os
import json
from gtts import gTTS
import sys
from config import SPEECH_PATH

def generate_speech_file_from_json_tts(json_file_name: str, output_file_name: str=None):
    """
    Generate a speech file from a JSON file using the gTTS library.

    Args:
        json_file_name (str): The name of the JSON file containing gTTS parameters.
        output_file_name (str, optional): The name of the output audio file. If not provided, will create same name as JSON file with .mp3 extension.
    """
    json_file_path = os.path.join(SPEECH_PATH, json_file_name)
    with open(json_file_path, "r") as f:
        gtts_params = json.load(f)
    tts = gTTS(**gtts_params)

    audio_file_path = None
    if output_file_name:
        audio_file_path = os.path.join(SPEECH_PATH, output_file_name)
    else:
        audio_file_path = json_file_name.replace('.json', '.mp3')
    
    print(f"Generating tts audio file.source: {json_file_path}\n\tdestination: {audio_file_path}")
    tts.save(audio_file_path)


if __name__ == "__main__":
    generate_speech_file_from_json_tts(sys.argv[1])