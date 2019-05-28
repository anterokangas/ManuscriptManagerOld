import os

from pydub import playback
from playsound import playsound
from simpleaudio import play_buffer
import winsound
from manuscript.tools.counter import Counter


def play_sound(sound):
    if sound is not None:
        prefix = "tmp"
        with Counter(prefix) as counter:
            tmp_file = os.path.join(".", prefix + f"_{counter:010d}.mp3")
            sound.export(tmp_file)
            playsound(tmp_file)
            os.remove(tmp_file)
