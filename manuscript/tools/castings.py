"""
Castings
"""
import shlex
import copy

import manuscript.tools.constants as mc
import manuscript.exceptions.exceptions as mex


SUPPORTED_LANGUAGES = {
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'bn': 'Bengali',
    'ca': 'Catalan',
    'zh': 'Chinese',
    'zh-cn': 'Chinese (Mandarin/China)',
    'zh-tw': 'Chinese (Mandarin/Taiwan)',
    'zh-yue': 'Chinese (Cantonese)',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'en-au': 'English (Australia)',
    'en-uk': 'English (United Kingdom)',
    'en-us': 'English (United States)',
    'eo': 'Esperanto',
    'fi': 'Finnish',
    'fr': 'French',
    'de': 'German',
    'el': 'Greek',
    'hi': 'Hindi',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'id': 'Indonesian',
    'it': 'Italian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'la': 'Latin',
    'lv': 'Latvian',
    'mk': 'Macedonian',
    'no': 'Norwegian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pt-br': 'Portuguese (Brazil)',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sr': 'Serbian',
    'sk': 'Slovak',
    'es': 'Spanish',
    'es-es': 'Spanish (Spain)',
    'es-us': 'Spanish (United States)',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'ta': 'Tamil',
    'th': 'Thai',
    'tr': 'Turkish',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
}


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
        raise mex.MMValueError(f"*** {object_} cannot be converted to int: {e}")


def language(lang):
    if lang in SUPPORTED_LANGUAGES:
        return lang

    raise mex.MMValueError(
        f"*** ValueError: language code '{lang}' is not supported.\n{supported_languages()}")


def supported_languages_as_text():
    text_ = "\nThe supported languages are:"
    length = max([len(key) for key in SUPPORTED_LANGUAGES])
    for key, value in SUPPORTED_LANGUAGES.items():
        text_ += f"\n{' ':5}{key:{length}}: {value}"
    return text_


def str_(object_):
    return None if object_ is None else str(object_)
