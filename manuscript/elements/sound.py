import os
from pydub import AudioSegment
from playsound import playsound

from manuscript.elements.definition import Definition
from manuscript.elements.action import Action

from manuscript.tools.castings import list_
from manuscript.tools.castings import as_is
import manuscript.tools.constants as mc
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

    def __init__(self, work, **kwargs):
        """ Define Sound object """
        print(f"Sound.__init__: {kwargs}")
        self.params = [{**dp, **sp} for dp, sp in zip(Sound.params, self.params)]
        super().__init__(work, **kwargs)
        #
        # Process input == list of sound/files
        #
        print(f"Sound: self.input={self.input}")
        sounds = [Sound.get_audio(self.work, sf) for sf in self.input]
        # Process other parameters before join
        # ---
        # Join
        print(f"Sound.init sounds={sounds}")
        audio = None
        for sound in sounds:
            if sound is None:
                self.audio = None
                return
            if audio is None:
                audio = sound
            else:
                audio += sound
        self.audio = audio


        super().define_action()
        #play(self.audio)
        # message(self.work, "SO0010", self.name, self.audio)

    @classmethod
    def from_audio(cls, work, **kwargs):
        """ Create a Sound object from audio segnment

        Parameters
        ----------
        work :      Work object
            Current work, contains settings, and defining and defined actions
        kwargs :    dict
            parameters, must contain 'audio'

        Returns
        -------
        Sound object
        """
        # Accept only those kwargs that are also Sound attributes
        audio = kwargs.pop("audio", None)
        if audio is None:
            raise ValueError(f"*** Trying to create Sound object from audio without audio")
        # print(f"Sound {Sound.pkeys}")
        kwargs = {key: kwargs[key] for key in
                  set(kwargs.keys()).intersection(Sound.pkeys)}
        # print(f"..> kwargs={kwargs}")
        obj = cls(work, **kwargs)
        obj.audio = audio

        #message(self.work, f"New Sound Element {obj.name} created."
        #        f"The new sound is:",
        #        obj.audio)
        return obj

    def do(self, **kwargs):
        """
        Do Sound object call

        Play, process or combine Sound object(s)

        Parameters
        ----------
        kwargs : dict
            Parameters
        Returns
        -------
        None
        """
        """
        Sound-objectilla 
        - jos on input, haetaan ne
        
        """
        print(f"Sound.do(self={self}")
        audio = self.audio
        if audio is not None:
            return audio
        # Lazy object, create new object and execute it
        new_sound = Sound(**self.__dict__)
        return new_sound(**kwargs)

        # if kwargs.get("input", "") == "":
        #     try:
        #         kwargs["input"] = self.name
        #         # except Exception as e:
        #         # print(f"Failed {e}")
        #     finally:
        #         pass
        #
        # super().do(**kwargs)
        # sounds_and_files = self.input
        #
        # sounds = []
        # for sound_or_file in sounds_and_files:
        #     sound = Sound.get_audio(self.work, sound_or_file)
        #     print(f"Sound.do: {sound_or_file} {sound}")
        #     if sound is not None:
        #         # process sound and join using parameters
        #         sounds.append(sound)
        # if len(sounds) == 0:
        #     return None
        # add_sound(sounds[0])
        #
        # Make new SOUND
        # if kwargs.get(SOUND, None) is not None:
        #    self.audio =
        #
        #
        # Export sound
        #
        # export = kwargs.pop("export", "")
        # if export != "":
        #     sounds[0].export(export)
        # # Play resulting sound (later: join)
        # for sound in sounds:
        #     print(sound)
        #     play(sound)
        #
        # return sound

    @classmethod
    def get_audio(cls, work, sound_or_file):
        """ Audiosegmment from sound object or mp3 file

        If not a sound object then search data dictionaries

        Parameters
        ----------
        work :  Work object
            Current work, contains settings and defining and defined actions
        sound_or_file : str
            Name of either a Sound object or an mp3 file

        Returns
        -------
        AudioSegment
            The audiosegment

        Raises
        ------
        MMFileNotFoundError
            If Sound not found
        """
        # sound_or_filesound_or_file is
        # either _ONE_ SOUND name or filename
        settings = work.defined_actions[mc.SETTINGS]
        sound_or_file = remove_quotes(sound_or_file)
        sound_name = work.defined_actions.get(sound_or_file, None)
        print(f"Sound::get_audio {sound_or_file}->{sound_name}")
        print("Defined actions:")
        for key, value in work.defined_actions.items():
            print(f"   {key:15}: {value}")
        if sound_name is not None:
            return sound_name.audio
        for data_dir in settings.data_dirs:
            try:
                sound = AudioSegment.from_mp3(
                    os.path.join(
                        data_dir,
                        sound_or_file))
                return sound
            except IOError:
                pass
        # Perhaps lazy evaluation
        return None
        raise ValueError(f"*** Sound or file '{sound_or_file}' not found")
