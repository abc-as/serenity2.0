import os
from gtts import gTTS
import pygame
from django.conf import settings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def synthesize_and_play_speech(text, filename):
    tts = gTTS(text=text, lang='en')

    media_path = os.path.join(settings.MEDIA_ROOT, 'text-to-speech', filename)
    os.makedirs(os.path.dirname(media_path), exist_ok=True)
    tts.save(media_path)

    pygame.mixer.init()

    return media_path
