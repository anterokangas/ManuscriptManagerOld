from manuscript.actions.definition import Definition
import manuscript.tools.constants as mc
from manuscript.tools.castings import list_


class Group(Definition):
    """ Definition of Group object and action"""
    params = [
        {'members': (list_, None)},
        {'gain': (float, 1.0)},
        {}
    ]

    def __init__(self, work, **kwargs):
        """ Define Group object """
        super().__init__(work, **kwargs)

    def do(self, **kwargs):
        """
        Do Group object call == call at the same time all members
        :param kwargs: parameters that temporary overrides declared values
        :return: None
        """
        text_ = kwargs.pop(mc.VALUES, "")
        me = super().do(**kwargs)
        for member in me.members:
            print(f"member {member}: {vars(self.work.defined_actions[member])}" )



# --------------------------------------------------
# Add the class to defined actions
# --------------------------------------------------
Definition.defining_actions[mc.GROUP] = Group
