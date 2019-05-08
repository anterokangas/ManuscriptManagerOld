import manuscript.language.constants as mc


class Definition:
    """ Super class for defining actions """
    params = [{"name": (str, None)},    #  Required (== not overriddable)
              {mc.VALUES: (str, "")},   #  Optional
              {}]                       #  Dependent

    defining_actions = {}   # add defining actions == subclasses

    defined_actions = {}   # add defined actions == objects of subclasses

    manuscript = []

    def __init__(self, **kwargs):
        """
        Initialize Manuscript Element Object
        ------------------------------------
        :param object: object to be initialized
        :param params: list of dicts of parameters: [required, optional, dependent]
                       each element of dict key {(convert_function, default_value)}
        :param kwargs: list of read parameters {key: value}
        :return: None
        """
        assert isinstance(self.params, list)
        assert len(self.params) == 3

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
                raise ValueError(f"*** Required parameter '{param}' missing")
            if param == 'input':
                print(
                    f"super__init0 after func {param} = {self.__dict__[param]}")

        #
        # Set optional parameters (default_value = name of the attribute)
        #
        for param, (func, default_value) in {**Definition.params[1], **self.params[1]}.items():
            val = kwargs.get(param, None)
            if val is not None:
                setattr(self, param, func(val))
            else:
                setattr(self, param, default_value)
            if param == 'input':
                print(
                    f"super__init1 after func {param} = {self.__dict__[param]}")
                print(f"That is {self.input}")
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
                val = settings.__dict__.get(default_value, None)
            if val is not None:
                setattr(self, param, func(val))
            else:
                raise ValueError(f"*** The parameter that {param} is dependent on is not set")
            if param == 'input':
                print(
                    f"super__init2 after func {param} = {self.__dict__[param]}")
        #
        # test if non-defined parameters
        #
        for kwarg in kwargs:
            if self.__dict__.get(kwarg, None) is None:
                raise ValueError(f"*** Non-defined parameter '{kwarg} = {kwargs[kwarg]}' in {self.__dict__}")

    def do(self, **kwargs):
        """
        Do defined action
        :param kwargs: Check and override parameters temporary
        :return: Overridden copy of object self
        """
        me = copy.deepcopy(self)
        for key, value in kwargs.items():
            if key == "params":
                continue
            if key not in vars(me):
                raise ValueError(f"*** {me.name} Trying to override non defined attribute '{key}'")
            # Required parameters == params[0] are not allowed to be overridden
            if key in self.params[0] and value != None:
                raise ValueError(f"*** {me.name} Trying to override required attribute '{key}'")
            #
            # Find conversion function and set attribute
            #
            func = self.params[0].get(key,
                       self.params[1].get(key,
                           self.params[2].get(key, ("", (str, "")))))[0]

            if key == mc.VALUES:
                print(f"==>\nkey={key}\nvalue={value}\nfunc={func}\nfunc(value)={func(value)}")
            setattr(me, key, func(value))
        return me

