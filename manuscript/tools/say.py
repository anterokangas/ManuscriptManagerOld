from gtts import gTTS
from pydub import AudioSegment
from tempfile import NamedTemporaryFile


def say(text_, lang="en"):
    #print(f"say: text_={text_} lang={lang}")
    if text_ == "":
        return
    tts = gTTS(text=text_,
               lang=lang)
    tf = NamedTemporaryFile(delete=False)
    tmp_file = tf.name
    tts.save(tmp_file)
    return AudioSegment.from_mp3(tmp_file)
