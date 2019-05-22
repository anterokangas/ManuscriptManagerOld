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

    def __init__(self, **kwargs):
        """ Define Wait object """
        super().__init__(**kwargs)

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
        if text != "" and time != "":
            raise ValueError(message_text("WA80101", (text_, time)))
        if text_ == "":
            add_silence(me.time)
