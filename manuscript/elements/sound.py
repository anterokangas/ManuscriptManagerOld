import os
from pydub import AudioSegment
from playsound import playsound

from manuscript.elements.definition import Definition
from manuscript.elements.action import Action

import manuscript.tools.audio as audio
from manuscript.tools.castings import as_is, bool_, list_
import manuscript.tools.constants as mc
import manuscript.exceptions.exceptions as mex
from manuscript.tools.process_sound import reverse_audio
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
         "overlay": (bool_, False),
         "reverse": (bool_, False),
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
        self.params = [{**dp, **sp} for dp, sp in zip(Sound.params, self.params)]
        super().__init__(work, **kwargs)

        sounds = [Sound.get_audio(self.work, sf) for sf in self.input]
        # TODO: Process other parameters before join
        if self.overlay:
            self.audio = audio.overlay(sounds)
        else:
            self.audio = audio.join(sounds)
        if self.audio is not None and self.reverse:
            self.audio = reverse_audio(self.audio)
            self.reverse = False
        super().define_action()

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
        name = kwargs.get('name', None)
        if name is None:
            raise mex.MMParameterError(f"*** ParameterError: Trying to created Sound.from_audio by name {name}")
        audio_ = kwargs.get("audio", None)
        if audio_ is None:
            raise mex.MMParameterError(f"*** ParameterError: Trying to create Sound object from audio without audio")
        kwargs = {key: kwargs[key] for key in
                  set(kwargs.keys()).intersection(Sound.pkeys)}

        object_ = cls(work, **kwargs)
        object_.audio = audio_

        work.define_action(name, object_)

        #message(self.work, f"New Sound Element {obj.name} created."
        return object_

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
        """
        # audio is generatd only once
        if self.audio is not None:
            return self.audio
        me = super().copy(**kwargs)
        input_ = list_(" ".join(self.input)
                       + " " + kwargs.get(mc.VALUES, "")
                       + " " + kwargs.get("input", ""))
        sounds = [Sound.get_audio(self.work, sf) for sf in input_]
        # TODO: Process other parameters after/before join

        if self.overlay:
            self.audio = audio.overlay(sounds)
        else:
            self.audio = audio.join(sounds)

        if self.audio is not None and self.reverse:
            self.audio = reverse_audio(self.audio)
            self.reverse = False

        return self.audio


    @classmethod
    def get_audio(cls, work, sound_or_file):
        """ return Audiosegment object from sound object or mp3 file, Not found --> None

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
        settings = work.defined_actions[mc.SETTINGS]
        sound_or_file = remove_quotes(sound_or_file)
        sound_name = work.defined_actions.get(sound_or_file, None)

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

    def copy(self, *args, **kwargs):
        return super().copy(*args, **kwargs)
