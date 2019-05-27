from manuscript.elements.role import Role

import manuscript.tools.audio as audio
from manuscript.tools.castings import list_
import manuscript.tools.constants as mc


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
        return audio.overlay(audios)
