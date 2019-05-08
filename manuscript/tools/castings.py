"""
Castings
"""
import shlex


def bool_(input_):
    """ Convert boolean or string to boolean, also 'False' and 'F' to False
    bools --> actual value
    str and stripped uppercase is FALSE or F -> False
    str and not in FALSE; F --> bool()
    otherwise --> False
    """
    if isinstance(input_, str):
        input_ = input_.strip().upper()
    return bool(input_) \
        if isinstance(input_, bool) \
        or isinstance(input_, str) and input_ not in ["FALSE", "F"] \
        else False


def list_(input_):
    """ Convert sep-separated string to list """
    return shlex.split(str(input_), posix=False)


def as_is(object_):
    """ Do nothing """
    return object_
