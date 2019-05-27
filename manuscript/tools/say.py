import os
from gtts import gTTS
from pydub import AudioSegment
from manuscript.tools.counter import Counter
import manuscript.tools.constants as mc


def say(text_, lang=mc.DEFAULT_LANG):
    if text_ == "":
        audio = None
    else:
        tts = gTTS(text=text_, lang=lang)
        prefix = "tmp"
        with Counter(prefix) as counter:
            tmp_file = prefix + f"_{counter:010d}.mp3"
            tts.save(tmp_file)
            audio = AudioSegment.from_mp3(tmp_file)
            os.remove(tmp_file)
    return audio
