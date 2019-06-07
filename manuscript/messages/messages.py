from manuscript.elements.definition import Definition
from manuscript.elements.settings import Settings
from manuscript.tools.say import say
from manuscript.tools.play import play_sound


"""
Messsage naming letter + four numbers
- letter(s)
    "AC" -> Action
    "CO" -> (process) Commands
    "DE" -> Definition
    "G" -> Group 
    "ME" -> Messages
    "PL" -> Playlist
    "RO" -> Role
    "SE" -> Settings
    "SO" -> Sound
    "WA" -> Wait
- first number
    "0" -> part of text, the code is not added
    "1" -> Informatic message
    "4" -> Warning
    "8" -> Severe Error 
"""

MESSAGES = {
    "CO8010": {"en": "At line {}: Defining action '{}' - no values",
               "fi": "Rivillä {}: Määrittävä tominto '{}' ei arvoja "},
    "CO8020": {"en": "At line {}: Double{} definition {}",
              "fi": "Rivillä {}: Toiminto {} määritelty kahdesti {}"},

    "ME0010": {"en": "The Mp3 file  is ready. Just listen!",
               "fi": "Mp3 tiedosto on valmis. Kuuntelepa."},
    "ME4010": {"en": "Message code {} is not defined for language {}",
              "fi": "Message koodia {} ei ole määritelty kielelle {}"},

    "PL8010": {"en": "Lazy evaluation of {} has no action",
               "fi": "Komennon {} laiskaa evaluointia varten ei ole toimintoa."},

    "RO0010": {"en": "Created Role element {} with language {}",
              "fi": "Luotu Role-elementti {}, kielinä {}"},
    "RO8010": {"en": "Double language definition {} and {}",
              "fi": "Kaksinkertainen kielimäärittely {} ja {}"},
    "RO8020": {"en": "Lang-like Role element{} is not defined",
              "fi": "Lang_like Role-elementtiä {} ei ole määritelty"},
    "RO8030": {"en": "Action element {} is already defined",
              "fi": "elementti {} on jo määritelty"},

    "SO0010": {"en": "Sound element {} created. The new sound is {}",
               "fi": "Luotu Sound-elementti. Uusi ääni on {}"},

    "SE0010": {"en": "Settings created.",
               "fi": "Settings eli asetukset määritelty."},

    "WA8010": {"en": "Attribute 'time' defined twice: values='{}', time='{}'",
               "fi": "Atribuutti 'time' määritelty kahdesti: values={}, times={}"},

}

# Add codes to beginning of the texts
for code in MESSAGES:
    for lang, txt in MESSAGES[code].items():
        # Except, do no add if code start with number "0"
        if code[2] == "0":
            continue
        MESSAGES[code][lang] = code + ": " + txt


def message_text(work, text_, params=tuple()):
    """ Recognize used language and get the corresponding text."""
    print(f"message_text text_={text_}")
    message_texts = MESSAGES.get(text_, None)
    # define language for message
    if Settings is None:
        lang = 'en'
    else:
        lang = work.settings.default_lang

    warning = False

    print(f"(message -->lang_={lang}")
    # get text_
    # - if it is a defined code also the language must match
    # - otherwise it is the original text
    if message_texts is not None:
        text_ = message_texts.get(lang, text_)
    else:
        warning = True
    print(f"message_text: {text_} {lang} {warning}")
    return text_, lang, warning


def message(work, text_="", params=tuple(), sound=None):
    # check if text_ is message code
    if work.settings is None \
            or work.settings.play_while is not True \
            or len(text_) == 6 and text_[2] > '0':
        return

    text_, lang_, warning = message_text(work, text_, params)
    if warning:
        play_sound(say(MESSAGES["ME4010"].get(
            lang_,
            "Text of code ME4010 {} for lang {} missing.").format(text_, lang_)))
    # print(text_.format(*_params), lang_)
    # play(say(text_.format(*_params), lang_))

    print(text_, lang_)
    play_sound(say(text_, lang_))
    play_sound(sound)

