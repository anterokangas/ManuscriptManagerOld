import copy
from manuscript.tools.castings import as_is
import manuscript.tools.constants as mc
import manuscript.exceptions.exceptions as mex

from manuscript.tools.subclasses import get_all_subclasses


class Definition:
    """ Super class for defining elements
    Class variables
        params :    list of dicts of form {key: (function, default value)}
            Defines object's attributes, lists elements:
            [0] :   required parameters (default value None must be set), not allowed to be changed
            [1] :   optional (default value given)
            [2] :   default value is copied from a given attribute
                    search first from same object, then settings
        reserved_names :  list
            names that cannot be used as params

    Attributes
        work :  Work
            the work everything is bind, e.g. work.settings contains settings
        attributes defined in class variable params

    Methods:
        __init__
        * the final super().__init__, used in __init__ methods
        * sets work
        * combines params of different subclass levels
        * sets params by either the given params or by their default values
        * checks that only defined params are trued to set

        copy
        * used in do-methods

        defined_action
        * declares action to be defined

    """

    PARAM_GROUP_DESC = ["Required parameters",
                        "Optional parameters",
                        "Dependent parameters"]

    params = [{"name": (as_is, None)},   # Required (== not overriddable)
              {mc.VALUES: (str, "")},  # Optional, default value given
              {}]                      # Optional, default value from other filed or from settings
    reserved_names = {"params", "work", "reserved_names", "COMMAND", mc.VALUES, mc.DEFINING}
    illegal_combinations = set()

    def __init__(self, work, **kwargs):
        """ Create new object, the fil super().__init__

        Parameters
        ----------
        work :  Work
            The work which contain all rhe elements
        kwargs :    dict
            Given params
        """
        self.work = work                 # Tie elements to specific work
        self.params = self.get_params()  # Complete params
        self.illegal_combinations = self.get_illegal_combinations()  # Complete  illegal combinations of param values
        # print(self.get_params_as_text())
        # Set required parameters
        for param, (func, default_value) in self.params[0].items():
            val = kwargs.get(param, None)
            if val is not None:
                setattr(self, param, func(val))
            else:
                raise mex.MMParameterError(f"*** Required parameter '{param}' missing")

        # Set optional parameters (default_value = name of the attribute)
        for param, (func, default_value) in self.params[1].items():
            val = kwargs.get(param, None)
            if val is None:
                val = default_value
            setattr(self, param, func(val))

        # set dependent parameters
        #
        # search value in this order:
        #   1. kwargs == parameter is given in init
        #   2. default value from self
        #   3. default value from settings
        #   4. otherwise --> error
        for param, (func, default_value) in self.params[2].items():
            val = kwargs.get(param, None)
            if val is None:
                val = kwargs.get(default_value, None)
            if val is None:
                val = self.work.settings.__dict__.get(default_value, None)
            if val is not None:
                setattr(self, param, func(val))
            else:
                raise mex.MMParameterError(f"*** The parameter that '{param}'' is dependent on is not set")

        self.define_action()

        # test if non-defined parameters
        for kwarg in kwargs:
            """
            if defining and audio is not defined ==> OK
            """
            if self.__dict__.get(kwarg, None) is None:
                raise mex.MMParameterError(f"*** Non-defined parameter '{kwarg} = {kwargs[kwarg]}' in {self.__dict__}")

    def copy(self, **kwargs):
        """ Copy object and set new values from kwargs """
        me = copy.copy(self)

        for key, value in kwargs.items():

            # Check reserved parameters
            if key in self.reserved_names:
                raise mex.MMParameterError(f"*** Illegal parameter: '{key}'.")
            if key not in vars(me):
                raise mex.MMParameterError(f"*** '{value}' tried to set non defined attribute '{key}'")

            # Required parameters == params[0] are not allowed to be overridden
            if key in self.params[0] and value is not None:
                raise mex.MMParameterError(f"*** '{key}' tried to override required attribute '{key}'")
            #
            # Find conversion function and set attribute
            #
            func = self.params[0].get(
                key, self.params[1].get(
                    key, self.params[2].get(
                        key, ("", (str, "")))))[0]

            setattr(me, key, func(value))
        return me

    def define_action(self):
        """ Declare that action (==self) is defined in work """
        self.work.define_action(self.name, self)

    def get_reserved_names(self):
        """ Combine reserved words of each parent class and itself """
        self_cls = self.__class__
        reserved_names = set()
        for cls in self_cls.mro():
            reserved_names = reserved_names.union(
                cls.__dict__.get("reserved_names", set()))
        return reserved_names

    def get_params(self):
        """ Combine params of each parent class and itself """
        self_cls = self.__class__
        params = [{}, {}, {}]
        for cls in self_cls.mro():
            params = [{**pp, **cp}
                      for pp, cp in zip(params, cls.__dict__.get(
                          "params", [{}, {}, {}]))]
        return params

    def get_params_as_text(self):
        """ Combine to string the values of params of each parent class and itself """
        name = self.__dict__.get("name", "<NOT DEFINDED>")
        result = f"\nPARAMETERS OF ELEMENT: {name}"
        for param_group_index, param_group in enumerate(self.params):
            result += f"\n{self.PARAM_GROUP_DESC[param_group_index]}"
            length = max([15] + [len(key) for key in param_group])
            for key in param_group:
                value = self.__dict__.get(key, None)
                result += f"\n{' ':5}{key:{length}}: {value}"
        return result

    def get_illegal_combinations(self):
        """ Combine illegal params value combinations of each parent class and itself """
        self_cls = self.__class__
        illegal_combinations = []
        for cls in self_cls.mro():
            illegal_combinations += cls.__dict__.get("illegal_combinations", [])
        return illegal_combinations

    def evaluate_illegal_combinations(self):
        """ Return True iff any combination's true-part is true and false-part is false"""
        for combination in self.get_illegal_combinations():
            next_combination = False
            for true_condition_key, true_condition_value in combination.get(True, {}).items():
                if not self.__dict__[true_condition_key] == true_condition_value:
                    next_combination = True
                    break
            if next_combination:
                continue
            for false_condition_key, false_condition_value in combination.get(False, {}).items():
                try:
                    if self.__dict__[false_condition_key] == false_condition_value:
                        next_combination = True
                        break
                except KeyError:
                    # Missing value is != than anything
                    pass
            if not next_combination:
                return True
        return False
