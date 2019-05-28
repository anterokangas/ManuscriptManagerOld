import copy
import manuscript.tools.constants as mc
import manuscript.exceptions.exceptions as mex


class Definition:
    """ Super class for defining actions """
    params = [{"name": (str, None)},    # Required (== not overriddable)
              {mc.VALUES: (str, ""),    # Optional
               mc.SOUND: (str, "")},    # generate SOUND object
              {}]                       # Dependent

    def __init__(self, work, **kwargs):
        """
        Initialize Manuscript Element Object
        ------------------------------------
        :param object: object to be initialized
        :param params: list of dicts of parameters: [required, optional, dependent]
                       each element of dict key {(convert_function, default_value)}
        :param kwargs: list of read parameters {key: value}
        :return: None
        """
        self.work = work
        #
        # Complete params
        #
        self.params = [{**dp, **sp} for dp, sp in zip(Definition.params, self.params)]

        #
        # Set required parameters
        # Order: subclass's params can override superclass' params
        #
        for param, (func, default_value) in {**self.params[0], **Definition.params[0]}.items():
            val = kwargs.get(param, None)
            if val is not None:
                setattr(self, param, func(val))
            else:
                raise mex.MMParameterError(f"*** Required parameter '{param}' missing")
        #
        # Set optional parameters (default_value = name of the attribute)
        #
        for param, (func, default_value) in {**Definition.params[1], **self.params[1]}.items():
            val = kwargs.get(param, None)
            if val is None:
                val = default_value
            setattr(self, param, func(val))
        #
        # set dependent parameters
        #
        # look
        #   1. kwargs == given parameters
        #   2. default value from self
        #   3. default value from settings
        #   4. otherwise --> error
        #
        for param, (func, default_value) in {**Definition.params[2], **self.params[2]}.items():
            val = kwargs.get(param, None)
            if val is None:
                val = kwargs.get(default_value, None)
            if val is None:
                val = self.work.settings.__dict__.get(default_value, None)
            if val is not None:
                setattr(self, param, func(val))
            else:
                raise mex.MMParameterError(f"*** The parameter that {param} is dependent on is not set")
        #
        # test if non-defined parameters
        #
        for kwarg in kwargs:
            if self.__dict__.get(kwarg, None) is None:
                mex.MMParameterError(f"*** Non-defined parameter '{kwarg} = {kwargs[kwarg]}' in {self.__dict__}")

    def copy(self, **kwargs):
        """
        Do defined action
        :param kwargs: Check and override parameters temporary
        :return: Overridden copy of object self
        """
        me = copy.copy(self)
        try:
            name = me.name
        except AttributeError:
            name = "<unknown>"

        for key, value in kwargs.items():
            if key == "params":
                continue
            if key == "name":
                continue
            if key not in vars(me):
                raise mex.MMParameterError(f"*** '{name}' trying to set non defined attribute '{key}'")
            # Required parameters == params[0] are not allowed to be overridden
            if key in self.params[0] and value is not None:
                raise mex.MMParameterError(f"*** '{name}' trying to override required attribute '{key}'")
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
        self.work.define_action(self.name, self)
