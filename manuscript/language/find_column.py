
def find_column(text, token):
    """ Compute column number

    Parameters
    ----------
    text :  str
        The parsed text
    token : sly.token
        The token whose positition is to find
    Returns
    -------
    int
        The corresponding column number
    """
    last_cr = text.rfind('\n', 0, token.index)
    if last_cr < 0:
        last_cr = 0
    column = (token.index - last_cr) + 1
    return column
