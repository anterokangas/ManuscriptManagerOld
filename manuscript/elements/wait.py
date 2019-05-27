from pydub import AudioSegment
from manuscript.elements.sound import Sound
import manuscript.tools.constants as mc


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
        if text_ != "":
            raise ValueError(message_text(self.work, "WA80101", (text_, "")))
        delay = kwargs.get("delay", "")
        print(f"delay={delay}")
        me = super().do(**kwargs)
        if delay != "":
            add_silence(duration=float(delay))
        else:
            add_silence(duration=me.delay)
