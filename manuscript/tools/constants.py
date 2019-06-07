"""
ManusscriptManager constants
import ...constants as mm
"""
import sys

# ------------------------------------
# Lexer and Parser
# ------------------------------------
# Language element names
COMMAND = "__COMMAND__"
COMMENT = "__COMMENT__"
VALUES = "__VALUES__"
DEFINING = "__DEFINING__"
NON_DEFINED = (None,)  # Must be non-string and not None!


# Defining actions
ROLE = "ROLE"
SOUND = "SOUND"
GROUP = "GROUP"
WAIT = "WAIT"
SETTINGS = "SETTINGS"
DEBUG = "DEBUG"


# Initiallly defined Actor names
NARRATOR = "NARRATOR"
MESSENGER = "__MESSENGER__"
BREAK = "BREAK"

# Other constants
DEFAULT_LANG = "en"
EPSILON = sys.float_info.epsilon

# ----------------
# Format text
# ----------------
ALIGN_CODES = {"LEFT": "<", "RIGHT": ">", "CENTER": "^"}
PAGE_WIDTH = 66
PAGE_LENGTH = 80
LEFT_MARGIN = 5
RIGHT_MARGIN = 5

LEFT = "LEFT"
CENTER = "CENTER"
RIGHT = "RIGHT"
HYPHEN = "-"
HINT = "#"

ALIGN = LEFT
CAPS = False
UNDERLINE = ""
LEADING_NEWLINE = True
TRAILING_NEWLINE = False
MIN_WIDTH = 10
MAX_WIDTH = 40
