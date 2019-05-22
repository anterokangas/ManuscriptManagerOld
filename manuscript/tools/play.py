import os
import playsound
from manuscript.tools.counter import Counter


def play(sound):
    print(f"play: {type(sound)}")
    if sound is not None:
        print(f"play: {len(sound)}")
        prefix = "tmp"
        with Counter(prefix) as counter:
            tmp_file = prefix + f"_{counter:010d}.mp3"
            print(f"'{tmp_file}'")
            sound.export(tmp_file)
            playsound.playsound(tmp_file)
            os.remove(tmp_file)