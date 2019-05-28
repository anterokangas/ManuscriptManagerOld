ESCAPE_CODE = "\033["
COLORS = {'black': 30, 'red': 31, 'green':32, 'yellow': 33, 'blue': 34, 'purple': 35, 'cyan': 36, 'white': 37}
BRIGHTS = {"bright "+color: value + 60 for color, value, in COLORS.items()}
TEXT_COLOR = {'reset': 0, **COLORS, **BRIGHTS}
TEXT_STYLE = {'reset': 0, 'no effect': 0, 'bold': 1, 'underline': 2, 'negative1': 3, 'negative2': 5}
BACKGROUND_COLOR = {color: value+10 for color, value in TEXT_COLOR.items()}
BACKGROUND_COLOR['reset'] = 0
RESET = (ESCAPE_CODE + "0;0;0m")


def highlight(text_, color='reset', style='reset', background='reset'):
    """ Decorate text using colors and other styles

    Parameters
    ----------
    text_ : str
        The text to be decorated
    color : str
        Code of the text color
    style : str
        Code of the text style
    background : str
        Code of the background style

    Returns
    -------
    str
        Decorated text
    """
    """
    Use color and other highlights
    :param text_: text to be highlighted
    :param color: text color
    :param style: text style (reset==no effect |b old | underline | etc.)
    :param background: background color
    :return: escape-coded highlighted string, rest-code in the end
    """
    return (ESCAPE_CODE
            + str(TEXT_STYLE.get(style.lower(), 'no_effect')) + ";"
            + str(TEXT_COLOR.get(color.lower(), 'red')) + ";"
            + str(BACKGROUND_COLOR.get(background.lower(), 'black')) + "m"
            + str(text_)
            + RESET)

