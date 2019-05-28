""" Define user-defined Manuscript exceptions """

class MMError(Exception):
    """ Base class of all other exceptions """
    pass


class MMSyntaxError(MMError):
    """ Raised when manuscript has syntax error """
    pass


class MMValueError(MMError):
    pass


class MMParameterError(MMError):
    pass


class MMNotDefiningActionError(MMError):
    pass


class MMDirectoryNotFoundError(MMError):
    pass


class MMFileNotFoundError(MMError):
    pass
