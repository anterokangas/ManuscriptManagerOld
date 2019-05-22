import os
from pydub import AudioSegment

from manuscript.elements.definition import Definition
from manuscript.elements.action import Action

import manuscript.tools.constants as mc

#from manuscript.messages.messages import message

from manuscript.tools.castings import list_
from manuscript.tools.castings import as_is
from manuscript.tools.play import play
from manuscript.tools.quotes import remove_quotes


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
    COMMAND = mc.SOUND
    params = [
        {},     # new name
        {mc.VALUES: (str, None),
         "gain": (float, 1.0),
         "input": (list_, ""),    # (sound|filename)
         "audio": (as_is, None),  # possible AudioSegment object
         "export": (str, ""),     # save sound
         "start": (int, 0),
         "end": (int, -1),
         "remove_start": (int, -1),
         "remove_end": (int, 0)},
        {}
    ]
    pkeys = set().union(params[0].keys(), params[1].keys(), params[2].keys())
    pkeys = pkeys.union(Action.params[0].keys(), Action.params[1].keys(), Action.params[2].keys())
    pkeys = pkeys.union(Definition.params[0].keys(), Definition.params[1].keys(), Definition.params[2].keys())

    def __init__(self, **kwargs):
        """ Define Sound object """
        super().__init__(**kwargs)
        #
        # Process input == list of sound/files
        #
        sounds = [Sound.get_audio(sf) for sf in self.input]
        # Process other parameters before join
        # ---
        # Join
        if sounds:
            audio = sounds[0]
            for sound in sounds[1:]:
                audio += sound
            self.audio = audio
        else:
            self.audio = None

        # message("SO0010", self.name, self.audio)

    @classmethod
    def from_audio(cls, **kwargs):
        # Accept only those keargs that are also Sound attributes
        audio = kwargs.pop("audio", None)
        if audio is None:
            raise ValueError(f"*** Trying to create Sound object from audio without audio")
        # print(f"Sound {Sound.pkeys}")
        kwargs = {key: kwargs[key] for key in
                  set(kwargs.keys()).intersection(Sound.pkeys)}
        # print(f"..> kwargs={kwargs}")
        obj = cls(**kwargs)
        obj.audio = audio

        #message(f"New Sound Element {obj.name} created."
        #        f"The new sound is:",
        #        obj.audio)
        return obj

    def do(self, **kwargs):
        """
        Do Sound object call
        :param kwargs: overriding parameters
        :return: None
        """

        #print(f"\n1 Sound.__do__({self}):")
        #for key, value in kwargs.items():
        #    print(f">{key} = {value}")
        if kwargs.get("input", "") == "":
            try:
                kwargs["input"] = self.name
        #        print(f" x Sound.do ()->sounds={kwargs['input']}")
            except Exception as e:
        #        print(f"Failed {e}")
                pass
        #print("\n2 Sound.__do__():")
        #for key, value in kwargs.items():
        #    print(f">>{key} = {value}")

        super().do(**kwargs)
        #print(f">>>  Sound.do ()->input={self.__dict__}")
        sounds_and_files = self.input

        sounds = []
        for sound_or_file in sounds_and_files:
            sound = Sound.get_audio(sound_or_file)
            if sound is not None:
                # process sound and join using parameters
                sounds.append(sound)
        #print(f">> sounds={sounds}")
        #print(f"call add_sound {sounds[0]} {type(sounds[0])}")
        if len(sounds) == 0:
            return
        #add_sound(sounds[0])
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
        # Always play resulting siund
        for sound in sounds:
            play(sound)


    @classmethod
    def get_audio(cls, sound_or_file):
        """
        :param sound_or_file: string: name of SOUND object or filename
        :return: AudioSegment object
        """
        # sound_or_filesound_or_file is
        # either _ONE_ SOUND name or filename
        sound_or_file = remove_quotes(sound_or_file)
        sound_name = Definition.defined_actions.get(sound_or_file, None)
        if sound_name is None:
            for sound_directory in Definition.settings.sound_directories:
                try:
                    sound = AudioSegment.from_mp3(
                        os.path.join(
                            sound_directory,
                            sound_or_file))
                    return sound
                except IOError:
                    pass
            raise ValueError(f"*** Sound or file '{sound_or_file}' not found")
        else:
            sound = sound_name.audio
        return sound
