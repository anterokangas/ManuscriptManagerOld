# TODO: make speak and say and Sound.audio be audio-elements

from pydub.audio_segment import AudioSegment
import os
import playsound
from manuscript.tools.counter import Counter


class Audio:
    """ Otherwise AudioSegment but emty == None """

    def __init__(self, audio_segment=None):
        self.audio_segment = audio_segment

    def append(self, audio_segment):
        """ """
        if audio_segment is None:
            return
        if self.audio_segment is None:
            self.audio_segment = audio_segment
        else:
            self.audio_segment += audio_segment

    @classmethod
    def join(cls, audio_segments=[]):
        """ join list of Audiosegments to one audio """
        audio = Audio()
        for audio_segment in audio_segments:
            audio.append(audio_segment)
        return audio.audio_segment

    def __add__(self, other):
        self.append(other.audiosegmant)

    def __len__(self):
        if self.audio_segment is None:
            return 0
        else:
            return len(self.audio_segment)

    def play(self, block=True):
        if self.audio_segment is not None:
            prefix = "tmp"
            with Counter(prefix) as counter:
                tmp_file = prefix + f"_{counter:010d}.mp3"
                self.audio_segment.export(tmp_file)
                playsound.playsound(tmp_file, block=block)
                os.remove(tmp_file)

    def export(self, filename):
        if self.audio_segment is None:
            os.remove(filename)
        else:
            self.audio_segment.export(filename)