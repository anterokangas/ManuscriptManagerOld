from manuscript.elements.definition import Definition
import manuscript.tools.constants as mc
#from manuscript.messages.messages import message
from manuscript.tools.castings import bool_, list_
import manuscript.tools.format as fmt


class Settings(Definition):
    """ Definition of Group object and action"""
    COMMAND = mc.SETTINGS
    params = [
        {"name": (str, mc.SETTINGS)},
        {"default_lang": (str, "fi"),
         "data_dirs":
             (lambda x: list_(". sound "+x, tail=""),
              ". sound"),  # Notice: add, not replace
         mc.VALUES: (str, ""),
         # TODO: text export
         # text
         "page_width": (int, mc.PAGE_WIDTH),
         "page_length": (int, mc.PAGE_LENGTH),
         "text_export": (str, "output.txt"),
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
        """ Define Settings object """
        #
        # defining_actios
        # defined_actions
        # settings          Setting-obj
        #
        print(f"Settings.__init__ kwargs={kwargs}")
        kwargs["name"] = mc.SETTINGS
        super().__init__(**kwargs)
        Settings.settings = self
        # Definition.defined_actions[mc.NARRATOR].lang = \
        #     Definition.settings.default_lang
        # copy self's attributes to class variables
        for key, value in self.__dict__.items():
            if key == 'params':
                continue
            setattr(Settings, key, value)
        print(f"Settings -->\n{self.__dict__}")
        for key, value in self.__dict__.items():
            print(f"{key}-->{value}")
        print(f"Settings.defined_actions={Settings.defined_actions}")
        print(f"Settings.defined_actions.get(mc.NARRATOR, None)={Settings.defined_actions.get(mc.NARRATOR, None)}")
        if Settings.defined_actions.get(mc.NARRATOR, None) is not None:
            print("NARRATOR")
            for key, value in Settings.defined_actions[mc.NARRATOR].items():
                print(f"{key}-->{value}")
            print(f'Settings.producer.settings.__dict__.get("default_lang")={Settings.producer.settings.__dict__.get("default_lang")}')
            Settings.defined_actions[mc.NARRATOR].lang = \
                Settings.producer.settings.__dict__.get("default_lang")
            print(f"Settings: init NARRATOR.lang={Settings.defined_actions[mc.NARRATOR].lang}")
        #message("SE0010")
