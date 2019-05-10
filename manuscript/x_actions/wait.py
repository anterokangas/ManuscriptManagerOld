from manuscript.actions.definition import Definition
import manuscript.language.constants as mc


class Wait(Definition):
    """ Definition of Wait object and waiting """
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
            #  error
            raise ValueError(f"property 'time' defined twice: values='{text_}' time='{time}'")
        if text_ == "":
            add_silence(me.time)



# --------------------------------------------------
# Add the class to defined actions
# --------------------------------------------------
Definition.defining_actions[mc.WAIT] = Wait
