"""
Add and remove surrounding quotes if necessary
"""


def add_quotes(text_):
    """
    Add quotes around string if necessary

    Cases
    (1) no spaces --> no need
    (2) no "s --> surround by "..."
    (3) no 's --> surround by '...'
    (4) otherwise --> surround by "..." (anyway)

    Parameters
    ----------
    text_ : str
        text to be quoted

    Returns
    -------
    str
        quoted text

    """
    if " " not in text_:
        # No need to add quotes
        return text_
    if '"' not in text_:
        return '"' + text_ + '"'
    if "'" not in text_:
        return "'" + text_ + "'"
    return '"' + text_ + '"'


def remove_quotes(text_):
    """
    Remove surrounding quotes if there is
    Parameters
    ----------
    text_ :  str
       text whose surrounding quotes are removev

    Returns
    -------
    str
        text without surrounding quotes
    """
    if len(text_) < 2:
        return text_
    if text_[0] == text_[-1] == "'" \
       or text_[0] == text_[-1] == '"':
        return text_[1:-1]
    return text_
