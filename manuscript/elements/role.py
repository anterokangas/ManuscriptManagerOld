import re

from manuscript.elements.action import Action
from manuscript.elements.sound import Sound

import manuscript.tools.constants as mc
from manuscript.tools.castings import bool_
from manuscript.tools.say import say
from manuscript.tools.play import play

from manuscript.messages.messages import message_text


class Role(Action):
    """ Definition of Role object and dialogue """
    # params[required, optional, dependent]
    # (attribute name, type conversion function, default value)
    COMMAND = mc.ROLE
    params = [
        {},
        {"pitch": (float, 0.0),
         "speed": (float, 0.0),
         "gain": (float, 1.0),
         "noname": (bool_, False),        # name is never spoken
         "lang_like": (str, mc.NARRATOR), # speak as 'like' except lang, default text == alias
         "audio_like": (str, ""),
         "text_like": (str, ""),
         "paragraph": (str, ""),          # paragraph format
         "left_margin": (int, mc.LEFT_MARGIN),
         "right_margin": (int, mc.RIGHT_MARGIN),
         "align": (str, mc.ALIGN),
         "caps": (bool_, mc.CAPS),
         "underline": (str, mc.UNDERLINE),
         "leading_newline": (bool_, mc.LEADING_NEWLINE),
         "trailing_newline": (bool_, mc.TRAILING_NEWLINE)
        },
        {"alias": (str, "name"),          # default value == dependent on
         "lang": (str, "default_lang")}   # look first self, then settings
    ]

    def __init__(self, work, **kwargs):
        """ define Role object """
        print(f"Role.init {kwargs}")
        super().__init__(work, **kwargs)
        super().define_action()
        #message(work, "RO0010", (self.name, self.lang))

    def speak(self, text_):
        """ Convert text to AudioSegment (sound) object"""
        # If the line contais only following special chars, it is considered ass empty
        if re.sub('[(){}<> .!?,;]', '', text_) == "":
            # Nothing to say!
            return None
        sound = say(text_, lang=self.lang)
        sound = Role.speed_change(sound, self.speed)
        sound = Role.pitch_change(sound, self.pitch)
        return sound

    @classmethod
    def speed_change(cls, sound, speed=0.0):
        # Manually override the frame_rate. This tells the computer how many
        # samples to play per second
        speed = 1.0 + speed / 10  # Tune speed value easier to use
        sound_with_altered_frame_rate = \
            sound._spawn(sound.raw_data,
                         overrides={"frame_rate": int(sound.frame_rate * speed)})
        # convert the sound with altered frame rate to a standard frame rate
        # so that regular playback programs will work right. They often only
        # know how to play audio at standard frame rate (like 44.1k)
        return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

    @classmethod
    def pitch_change(cls, sound, pitch=0.0):
        pitch /= 10  # Tune pitch value easier to use
        new_sample_rate = int(sound.frame_rate * (2.0 ** pitch))
        sound_with_altered_pitch = \
            sound._spawn(sound.raw_data,
                         overrides={'frame_rate': new_sample_rate})
        return sound_with_altered_pitch

    def do(self, **kwargs):
        """
        Do Role object call
        Example:
         (A [text] [SOUND B)] [(lang_like AA)] [param])
         - parameters:
           text: the text to be spoken, default=A.alias
           SOUND: create Sound object B with audio=A.speak(text), empty: say
           lang_like: set lang=AA.lang
           params: Role params, override A's params, not allowed lang_like & lang
        - action:
          -- generate audio object
          -- if SOUND given
                create Sound object B (B.audio=A.speak(text)
                otherwise play audio

        :param kwargs: overriding parameters
        :return: None
        """
        print(f"Role.do {kwargs}")
        # ----------------------------------
        # text to speak
        # ----------------------------------
        text_ = kwargs.pop(mc.VALUES, "")
        if text_ == "":
            text_ = self.alias
            kwargs[mc.VALUES] = text_

        # ----------------------------------
        # override language
        # ----------------------------------
        lang_like = kwargs.pop("lang_like", "")
        lang = kwargs.get("lang", "")
        if lang_like != "" and lang != "":
            raise ValueError(message_text("self.work, RO8010", (lang_like, lang)))
        if lang_like != "":
            like = self.work.defined_actions.get(lang_like, None)
            if like is None or not isinstance(like, Role):
                raise ValueError(message_text(self.work, "RO8020", (lang_like,)))
            kwargs["lang"] = like.lang

        super().do(**kwargs)
        print(f"call speak({text_})")
        self.audio = self.speak(text_)
        print(f"audio.length={len(self.audio)}")

        #message(self.work, f"Created speak: {self.name} says,", audio)

        sound_name = kwargs.pop(mc.SOUND, "")
        if sound_name == "":
            return self.audio

        print(f"sound_name={sound_name}")
        if self.work.definition_allowed(sound_name):
            print(f"Create Sound.from_audio object")
            object_ = Sound.from_audio(self.work, name=sound_name, audio=self.audio, **kwargs)
            print(f"Sound.from_audio object created")
            return None
            return object_.audio

        if sound_name in self.work.defined_actions:
            sound_object = self.work.defined_actions[sound_name]
            if sound_object.audio is None:
                sound_object.audio = self.audio
                return None
            raise ValueError(f"*** {sound_name} already has audio")

        raise ValueError(message_text(self.work, "RO8030", (sound_name,)))
