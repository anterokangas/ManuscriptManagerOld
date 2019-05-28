from pydub import AudioSegment
from manuscript.elements.sound import Sound
import manuscript.tools.constants as mc
import manuscript.exceptions.exceptions as me
from manuscript.tools.process_sound import silence


class Wait(Sound):
    """ Definition of Wait object and waiting """
    COMMAND = mc.WAIT
    params = [
        {},
        {"delay": (float, 0.3)},
        {}
    ]

    def __init__(self, work, **kwargs):
        """ Define Wait object """
        #print(f"Wait.__init__: {kwargs}")
        kwargs["input"] = ""
        super().__init__(work, **kwargs)
        self.audio = silence(self.delay)
        super().define_action()

    def do(self, **kwargs):
        """
        Do Wait object call
        :param kwargs: overriding parameters
        :return: None
        """
        # both defined -> error
        text_ = kwargs.get(mc.VALUES, "")
        if text_ != "":
            raise mex.MMValueError(message_text(self.work, "WA80101", (text_, "")))

        me = super().copy(**kwargs)
        return silence(me. delay)


