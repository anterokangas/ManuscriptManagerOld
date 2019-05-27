import os
import playsound
from manuscript.tools.counter import Counter


def play(sound, block=True):
    if sound is not None:
        prefix = "tmp"
        with Counter(prefix) as counter:
            tmp_file = prefix + f"_{counter:010d}.mp3"
            sound.export(tmp_file)
            playsound.playsound(tmp_file, block=block)
            os.remove(tmp_file)
