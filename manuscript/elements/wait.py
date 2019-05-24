from pydub import AudioSegment
from manuscript.elements.sound import Sound
import manuscript.tools.constants as mc


class Wait(Sound):
    """ Definition of Wait object and waiting """
    COMMAND = mc.WAIT
    params = [
        {},
        {"time": (float, 0.5)},
        {}
    ]

    def __init__(self, work, **kwargs):
        """ Define Wait object """
        #print(f"Wait.__init__: {kwargs}")
        kwargs["input"] = ""
        super().__init__(work, **kwargs)
        super().define_action()

    def do(self, **kwargs):
        """
        Do Wait object call
        :param kwargs: overriding parameters
        :return: None
        """
        # text_ is alternative for time
        # both defined -> error
        text_ = kwargs.pop(mc.VALUES, "")
        time = kwargs.get(mc.VALUES, "")
        me = super().do(**kwargs)
        if text_ != "" and time == 0:
            raise ValueError(message_text(self.work, "WA80101", (text_, time)))
        if text_ == "":
            add_silence(duration=me.time)
