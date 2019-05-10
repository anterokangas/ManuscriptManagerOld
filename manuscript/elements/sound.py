import os
from pydub import AudioSegment

from manuscript.elements.definition import Definition
from manuscript.elements.action import Action
import manuscript.language.constants as mc
from manuscript.tools.castings import list_
from manuscript.tools.castings import as_is
from manuscript.tools.quotes import remove_quotes

def create_sound(sound_name, **kwargs):
    object_ = Sound(name=sound_name,
                    __VALUES__=add_quotes(sound_name), **kwargs)
    # object_ = Playlist.DEFINING_ACTIONS[mc.SOUND](
    #     name=sound_name, __VALUES__=add_quotes(sound_name), **kwargs)
    Definition.defined_actions[sound_name] = object_
    return sound_name, \
       object_, \
       {"name": sound_name, mc.VALUES: sound_name, **kwargs}


class Sound(Action):
    """ Define Sound object
    (SOUND name (input list of sounds and filenames  to be joined
    (gain g)  (start s) (end e)
    (cross_fade c) <-- not for the last (1 ==> error?)
    (fade_in fi) (fade_out fo)
    (overlay, position, gain_during_overlay, loop, times)
    (apply_gain, fade, from_gain , to_gain
    more: https://github.com/jiaaro/pydub/blob/master/API.markdown
    )
    """
    params = [
        {},     # new name
        {mc.VALUES: (str, None),
         "gain": (float, 1.0),
         "input": (list_, []),    # (sound|filename)*
         "audio": (as_is, None),  # possible AudioSegment object
         "export": (str, ""),     # save sound
         "start": (int, 0),
         "end": (int, -1),
         "remove_start": (int, -1),
         "remove_end": (int, 0)},
        {}
    ]

    def __init__(self, **kwargs):
        """ Define Sound object """
        print("\nSound.__init__():")
        for key, value in kwargs.items():
            print(f">{key} = {value}")
        super().__init__(**kwargs)
        #
        # Process input == list of sound/files
        #
        print(f"Sound.__init: {self.input}")
        sounds = [Sound.get_audio(sf) for sf in self.input]
        # Process other parameters
        #---
        # Join
        audio = sounds[0]
        for sound in sounds[1:]:
            audio += sound
        self.audio = audio

    @classmethod
    def from_audio(cls, **kwargs):
        # Accept only those keargs that are also Sound attributes

        print("\nSound.from_audio():")
        for key, value in kwargs.items():
            print(f">{key} = {value}")
        audio = kwargs.pop("audio", None)
        if audio is None:
            raise ValueError(f"*** Trying to create Sound object from audio without audio")

        kwargs = {key: kwargs[key] for key in
                  set(kwargs.keys()).intersection(
                      set(Sound.__dict__.keys()))}
        obj = cls(**kwargs)
        obj.audio = audio
        return obj


    def do(self, **kwargs):
        """
        Do Sound object call
        :param kwargs: overriding parameters
        :return: None
        """

        print("\n1 Sound.__do__():")
        for key, value in kwargs.items():
            print(f">{key} = {value}")
        if kwargs.get("input", "") == "":
            try:
                kwargs["input"] = self.name
                print(f" x Sound.do ()->sounds={kwargs['input']}")
            except Exception as e:
                print(f"Failed {e}")
                pass
        print("\n2 Sound.__do__():")
        for key, value in kwargs.items():
            print(f">>{key} = {value}")

        me = super().do(**kwargs)
        print(f">>>  Sound.do ()->sounds={me.input}")
        print(f"Sound._init__. input={me.input})")
        sounds_and_files = me.input
        #### VALUES --> input!!!!!
        sounds = []################VVVVVVV ON STRING!
        for sound_or_file in sounds_and_files:
            sound_or_file = remove_quotes(sound_or_file)
            print(f"-1->sound_or_file={sound_or_file}")
            sound = Definition.defined_actions.get(sound_or_file, None)
            print(f"-2---->sound={sound}")
            if sound is None:
                try:
                    sound = AudioSegment.from_mp3(sound_or_file)
                    print(f"-3------->sound={sound}")
                except:
                    print(f"*** Mp3 file {sound_or_file} not found, skipped.")
                    pass
            else:
                sound = sound.audio
                print(f"-4----------------->sound={sound}")
            if sound is not None:
                sounds.append(sound)
        print(f">> sounds={sounds}")
        print(f"call add_sound {sounds[0]} {type(sounds[0])}")
        add_sound(sounds[0])
        #
        # Make new SOUND
        #if kwargs.get(SOUND, None) is not None:
        #    self.audio =
        #
        #
        # Export sound
        #
        export = kwargs.pop("export", "")
        if export != "":
            sounds[0].export(export)

    @classmethod
    def get_audio(cls, sound_or_file):
        """
        :param sound_or_file: string: name of SOUND object or filename
        :return: AudioSegment object
        """
        # sound_or_filesound_or_file is
        # either _ONE_ SOUND name or filename
        print(f"1get_sound {sound_or_file}")
        sound_or_file = remove_quotes(sound_or_file)
        print(f"2get_sound {sound_or_file}")
        sound_name = Definition.defined_actions.get(sound_or_file, None)
        print(f"sound_name={sound_name}")
        if sound_name is None:
            for sound_directory in Definition.settings.sound_directories:
                print(f"sound_directory={sound_directory}:\n  {os.listdir(sound_directory)}")
                try:
                    name = os.path.join(
                        sound_directory,
                        sound_or_file)
                    print(f"trying to open mp3 file {name}")
                    sound = AudioSegment.from_mp3(
                        os.path.join(
                            sound_directory,
                            sound_or_file))
                    return sound
                except:
                    pass
            raise ValueError(f"*** Sound or file {sound_or_file} not found")
        else:
            sound = sound_name.audio
        return sound

# --------------------------------------------------
# Add the class to defined actions
# --------------------------------------------------
Definition.defining_actions[mc.SOUND] = Sound
