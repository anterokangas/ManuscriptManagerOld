from manuscript.actions.definition import Definition
import manuscript.tools.constants as mc
from manuscript.tools.castings import bool_
from manuscript.tools.castings import list_


class Settings(Definition):
    """ Definition of Group object and action"""
    params = [
        {"name": (str, mc.SETTINGS)},
        {"default_lang": (str, "fi"),
         "voice_directories":       # Notice: add, not replace
             (lambda x: list_(". voice "+x), ". voice"),
         mc.VALUES: (str, ""),
         # mp3 export
         "export": (str, "output.mp3"),
         "format": (str, "mp3"),
         "title": (str, ""),
         "artist": (str, "Various Artists"),
         "album": (str, ""),
         "comments": (str, ""),
         "date": (str, ""),
         "genre": (str, ""),
         "cover": (str, None),
         # play results in the end
         "play_final": (bool_, True),
         # show results
         "print_text": (bool_, False),
         "print_defined_actions": (bool_, False),
         "print_manuscript": (bool_, False),
         # debug settings
         "play_while": (bool_, False),
         "print_executions": (bool_, False)},
        {}
    ]

    def __init__(self, **kwargs):
        """ Define Group object """
        kwargs["name"] = mc.SETTINGS
        super().__init__(**kwargs)
        Definition.settings = self
        Definition.defined_actions[mc.NARRATOR].__dict__['lang'] = \
            Definition.settings.__dict__['default_lang']



# --------------------------------------------------
# Add the class to defined actions
# --------------------------------------------------
Definition.defining_actions[mc.SETTINGS] = Settings
