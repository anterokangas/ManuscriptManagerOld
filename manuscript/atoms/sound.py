import os
from operator import xor
from pydub import AudioSegment
from playsound import playsound

from manuscript.atoms.definition import Definition

import manuscript.tools.audio_tools as audio_tools
from manuscript.tools.castings import as_is, bool_, list_, str_
import manuscript.tools.constants as mc
import manuscript.exceptions.exceptions as mex
from manuscript.tools.process_sound import reverse_audio
from manuscript.tools.quotes import remove_quotes


class Sound(Definition):
    """  Sound - to generate sound object., play and save it

    1. (SOUND X [_params] (input Y Z)) -params-> X = Y+Z
    2. (X Y Z [_params] [(input U V))] -params-> X+Y+z+U+V can be lazy
    3. (X Y Z [_params][(input U V)] (SOUND W)) -params-> W=X+Y+Z+U+V can be lazy
    4. (SOUND X [_params] (input Y Z) (SOUND U)) -params-> error
    5. (ROLE/GROUP-name text [params] (SOUND X)) -params-> X = sound
    6. (Wait (delay n) (SOUND X)

    with (SOUND ::  __DEFINING__ is True  no (SOUND, no (audio

    ----------------------------
    1: no:name + values + input -> init-> create name(input)
    2. name + values + input + kw_input-> do init tmp(name+values+input+kw_input) + play
    3. name + input + kw_input + sound -> do init sound(name+values+input+kw_input)
    4. no:name + sound -> error
    ------------------------
    exec    E   x
    Class variables
        _COMMAND :   mc.SOUND (to collect _COMMAND-commands
        _params :    list of dicts to declare and redefined _params as in Definition
        * _params audio and input cannot be at same time: input when audio is not generated!
        param_keys :     set of all _params-keys for SOUND-class

    Attributes
        work :      Work
        attributes defined in class variable _params

    Class Methods
        from_audio
            creates new SOUND object by audio
        get_audio
            gets audio from SIUND-object or filename

    Methods
        __init__
            creates new SOUND object by input (ist of other SOUND ojects or filenames)
        do
            call SOUND-object: either has audio --> return audio,
                               or has not --> first creates audio, then returns it
        copy
            copies and resests values (by passing the call to super().copy()
    """



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
        {},
        {mc.SOUND: (str, ""),               # generate SOUND object (SOUND-name)
         mc.DEFINING: (bool, False),        # is the command just defining or not
         "gain": (float, 1.0),
         "input": (list_, ""),              # (sound/filename(s) separated by space)
         "audio": (as_is, mc.NON_DEFINED),  # possible AudioSegment object
         "overlay": (bool_, False),         # multiple sounds/files overlayed or concatenated
         "reverse": (bool_, False),         # reverse siund (once)
         "export": (str, ""),               # save sound
         "start": (int, 0),
         "end": (int, -1),
         "remove_start": (int, -1),
         "remove_end": (int, 0)},
        {}
    ]

    illegal_combinations = [{True: {mc.DEFINING: True}, False: {"audio": mc.NON_DEFINED}}]

    def __init__(self, work, **kwargs):
        """ Create Sound object
        Combine all parent class _params
        (SOUND (input X Y) (SOUND Z)) --> Sound-object Z = X+Y
        (X Y (input Z) (SOUND U)) --> Sound object U = X+Y+Z
        ~~ (SOUND U (input X Y Z))
        Parameters
        ----------
        work :  Work
            container of all elements
        kwargs : dict
            parameters
        """
        print(f"Sound.init: {kwargs.keys()}")
        # Either input (input and/or VALUES )or audio must be given (xor)
        audio = kwargs.get("audio", None)
        input = kwargs.get("input", "")
        name = kwargs.get("_name", "")
        values = kwargs.get(mc.VALUES, "")
        defining = kwargs.get(mc.DEFINING, False)

        # if defining is True audio shoukd not be given
        if defining and audio is not None:
            raise mex.MMParameterError(f"*** Defining SOUND command with audio is not allowed.")

        required_parameters = xor(audio is not None, input+values != "")
        if not required_parameters:
            raise mex.MMParameterError(f"*** Either audio or input (´+name+VALUES)  must be given")

        #self._params = [{**dp, **sp} for dp, sp in zip(Sound._params, self._params)]
        self.reserved_names = self.get_reserved_names()
        #self.param_keys = self.get_param_keys()
        super().__init__(work, **kwargs)

        if self.audio is None:
            input_ = list_(name + " " + values + input)
            audios = Sound.get_audios(work, input_)
            self.combine_audios(audios)

        if self.audio is not None:
            self.process_audio()

        super().define_action()

    def combine_audios(self, audios, **kwargs):
        """ Combine == overlay or join audio segments

        Parameters
        ----------
        audios : list of AudioSegments
            the segments to be combined
        kwargs

        Returns
        -------

        """
        if kwargs.get("overlay", self.overlay):
            self.audio = audio_tools.overlay(audios, **kwargs)
        else:
            self.audio = audio_tools.join(audios, **kwargs)


    def process_audio(self):
        if self.audio is None:
            return
        if self.reverse:
            self.audio = reverse_audio(self.audio)
            self.reverse = False

    @classmethod
    def from_audio(cls, work, **kwargs):
        """ Create a Sound object from audio segnment


        (SOUND X (input Y)) -> 1. sleeping SOUND-object X with input, 2. X.audio=Y.audio
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
        name = kwargs.pop("_name", None)
        if name is None:
            raise mex.MMParameterError(f"*** Trying to create Sound.from_audio by name {name}")

        audio = kwargs.pop("audio", None)
        if audio is None:
            raise mex.MMParameterError(f"*** ParameterError: Trying to create Sound.from_audio without audio")

        # Illegal names not allowed
        if not work.definition_allowed(name):
            raise mex.MMParameterError(f"*** Trying to create Sound.from audio by illegal name '{name}'")

        # Defined name allowed only if Sound without audio
        if name in work.defined_actions:
            raise mex.MMParameterError(f"*** Trying to Create Sound.from_audio by already defined name '{name}'")


        # class_param_keys = set()
        # for parent_class in cls.mro():
        #     for class_params in parent_class.__dict__.get("_params, []"):
        #         class_param_keys = class_param_keys.union(class_params.keys())
        #
        # kwargs = {key: kwargs[key] for key in
        #           set(kwargs.keys()).intersection(class_param_keys)}


        object_ = cls(work, name=name, audio=audio, **kwargs)
        work.define_action(name, object_)
        return object_

    def do(self, **kwargs):
        """
        Do Sound object call
        (X Y Z (input U V)) -> play X+Y+Z+U+V
        (X Y Z (input U V) (SOUND W)) -> create W=X+Y+Z+U+V
        if audio is not None --> process a copy
        else generate audio from input/values and process
        if SOUND --> create new SOUND-object

        Play, process or combine Sound object(s)

        Parameters
        ----------
        kwargs : dict
            Parameters
        Returns
        -------
        """
        if self.audio is None:
            # audio is generated only once
            me = self
            input_ = list_(self._name
                           + " ".join(self.input)
                           + " " + kwargs.get(mc.VALUES, "")
                           + " " + kwargs.get("input", ""))
            sounds = [Sound.get_audio(me._work, sf) for sf in input_]

            # sounds are either overlayed or joined
            me.combine_audios(sounds, **kwargs)
        else:
            me = self.copy(**kwargs)

        me.process_audio()

        sound_name = kwargs.get(mc.SOUND, "")
        if sound_name == "":
            return me.audio

        Sound.from_audio(me._work, name=sound_name, audio=me.audio)
        return None

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
        print(f"get_audio: sound_or_file={sound_or_file}")
        settings = work.defined_actions[mc.SETTINGS]
        sound_or_file = remove_quotes(sound_or_file)
        sound_name = work.defined_actions.get(sound_or_file, None)
        print(f"-->sound_name={sound_name}")
        if sound_name is not None:
            print(f"------>sound_name.audio={sound_name.audio}")
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


    @classmethod
    def get_audios(cls, work, sounds_or_files):
        print(f"get_audios: sound_of_files={sounds_or_files}")
        audios = []
        for sound_or_file in sounds_or_files:
            audio = Sound.get_audio(work, sound_or_file)
            if audio is None:
                return []
            audios.append(audio)
        return audios
