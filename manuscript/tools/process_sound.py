
from gtts import gTTS
from playsound import playsound
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
import re
import os
from manuscript.elements.definition import Definition
from manuscript.tools.quotes import remove_quotes


# class Playlist():
#     def __init__(self, sound=None):
#         self.playlist = sound
#
#     def append(self, sound):
#         if self.playlist is None:
#             self.playlist = sound
#         else:
#             self.playlist = self.playlist.append(sound)



def speak(text_, create_sound=None, prefix="tmp", **kwargs):
    """ Convert text to AudioSegment (sound) object"""
    if re.sub('[(){}<> .!?,;]', '', text_) == "":
        # Nothing to say!
        return
    tts = gTTS(text=text_,
               lang=kwargs['lang'])
    #  with Counter(prefix) as counter:
    #    tmp_file = prefix + f"_{counter:04d}.mp3"
    #    tts.save(tmp_file)

    tf = NamedTemporaryFile(delete=False)
    tmp_file = tf.name
    tts.save(tmp_file)
    sound = AudioSegment.from_mp3(tmp_file)

    speed = kwargs['speed']
    sound = speed_change(sound, speed)

    pitch = kwargs['pitch']
    sound = pitch_change(sound, pitch)

    if create_sound is None:
        append_to_playlist(sound)

        if settings.play_while:
            with Counter(prefix) as counter:
                tmp_file = prefix + f"_{counter:04d}.mp3"
                sound.export(tmp_file)

            print(f"speak playwhile tmp_file={tmp_file}")

            playsound(tmp_file)
            os.remove(tmp_file)
    return sound


def append_to_playlist(sound):
    global playlist
    if playlist is None:
        playlist = sound
    else:
        playlist = playlist.append(sound)


def speed_change(sound, speed=0.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    speed = 1.0 + speed/10  # Tune speed value easier to use
    sound_with_altered_frame_rate = \
        sound._spawn(sound.raw_data,
                     overrides={"frame_rate": int(sound.frame_rate * speed)})
    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


def pitch_change(sound, pitch=0.0):
    pitch /= 10  #  Tune pitch value easier to use
    new_sample_rate = int(sound.frame_rate * (2.0 ** pitch))
    sound_with_altered_pitch = \
        sound._spawn(sound.raw_data,
                     overrides={'frame_rate': new_sample_rate})
    return sound_with_altered_pitch


def add_sound(filename, **kwargs):
    """ Play mp3 file """
    print(f"addsound {filename} {type(filename)}")
    if isinstance(filename, Sound):
        sound = filename.audio
    elif isinstance(filename, AudioSegment):
        sound = filename
    else:
        sound = AudioSegment.from_mp3(filename)
    append_to_playlist(sound)
    if Definition.settings.play_while and not isinstance(filename, AudioSegment):
        playsound(filename)


def add_silence(time):
    """ Create silence (time in seconds)"""
    silence = AudioSegment.silent(time*1000)
    append_to_playlist(silence)



def get_sound(sound_or_file):
    # sound_or_filesound_or_file is
    # either _ONE_ SOUND name or filename
    print(f"1get_sound {sound_or_file}")
    sound_or_file = remove_quotes(sound_or_file)
    print(f"2get_sound {sound_or_file}")
    sound_name = Definition.defined_actions.get(sound_or_file, None)
    if sound_name is None:
        for voice_directory in Definition.settings.voice_directories:
            try:
                name = os.path.join(
                        voice_directory,
                        sound_or_file)
                print(f"trying to open mp3 file {name}")
                sound = AudioSegment.from_mp3(
                    os.path.join(
                        voice_directory,
                        sound_or_file))
                return sound
            except:
                pass
        raise ValueError(f"*** Sound or file {sound_or_file} not found")
    else:
        sound = sound_name.audio
    return sound