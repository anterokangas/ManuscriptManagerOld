"""
Castings
"""
import shlex
import copy


def bool_(input_):
    """ Convert boolean or string to boolean, also 'False' and 'F' to False
    bools --> actual value
    str and stripped uppercase is FALSE or F -> False
    str and not in FALSE; F --> bool()
    otherwise --> False
    """
    input_ = copy.copy(input_)
    if isinstance(input_, str):
        input_ = input_.strip().upper()
    return bool(input_) \
        if isinstance(input_, bool) \
        or isinstance(input_, str) and input_ not in ["FALSE", "F"] \
        else False


def list_(input_, tail=None):
    """ Convert sep-separated string to list
        Add empty string element to the end (for net addresses)
    """
    if tail is None:
        return shlex.split(str(input_), posix=False)
    else:
        return shlex.split(str(input_), posix=False) + [tail]


def as_is(object_):
    """ Do nothing """
    return object_


def int_(object_):
    try:
        return int(object_)
    except Exception as e:
        return e == 0
