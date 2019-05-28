from manuscript.elements.role import Role, Sound

import manuscript.exceptions.exceptions as mex

import manuscript.tools.audio as audio
from manuscript.tools.castings import list_
import manuscript.tools.constants as mc

from manuscript.messages.messages import message_text

class Group(Role):
    """ Definition of Group object and action """
    COMMAND = mc.GROUP
    params = [
        {'members': (list_, None)},
        {'gain': (float, 1.0)},
        {}
    ]

    def __init__(self, work, **kwargs):
        """ Define Group object """
        super().__init__(work, **kwargs)
        super().define_action()

    def do(self, **kwargs):
        """
        Do Group object call == call at the same time all members
        :param kwargs: parameters that temporary overrides declared values
        :return: None
        """
        text_ = kwargs.get(mc.VALUES, "")
        me = super().copy(**kwargs)
        audios = []
        for member in me.members:
            #print(f"\nmember {member}: {vars(self.work.defined_actions[member])}" )
            member_object_ = self.work.defined_actions[member]
            audios.append(member_object_.speak(text_))

        the_audio = audio.overlay(audios)
        sound_name = kwargs.get(mc.SOUND, "")
        if sound_name == "":
            return the_audio

        if self.work.definition_allowed(sound_name):
            Sound.from_audio(self.work, name=sound_name, audio=the_audio, **kwargs)
            return None

        if sound_name in self.work.defined_actions:
            sound_object = self.work.defined_actions[sound_name]
            if sound_object.audio is None:
                sound_object.audio = the_audio
                return None
            raise mex.MMValueError(f"*** {sound_name} already has audio")

        raise mex.MMValueError(message_text(self.work, "RO8030", (sound_name,)))
