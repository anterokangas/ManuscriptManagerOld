from manuscript.atoms.definition import Definition
import manuscript.tools.constants as mc
#from manuscript.messages.messages import message
from manuscript.tools.castings import bool_, list_, language


class Settings(Definition):
    """ Definition of Group object and action"""
    _COMMAND = mc.SETTINGS
    _params = [
        {"name": (str, mc.SETTINGS)},
        {"default_lang": (language, mc.DEFAULT_LANG),
         "data_dirs":
             (lambda x: list_(". data "+x, tail=None),
              ""),  # Notice: add, not replace
         "temp_dir": (str, "."),
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
         "cover": (str, ""),
         # play results in the end
         "play_final": (bool_, True),
         # show results
         "print_final_text": (bool_, False),
         # debug settings
         "play_while": (bool_, False),
         "print_supported_languages": (bool_, False),
         "print_defining_actions": (bool_, False),
         "print_defined_actions": (bool_, False),
         "print_manuscript_text": (bool_, False),
         "print_manuscript_parsed": (bool_, False),
         "print_executions": (bool_, False)},
        {}
    ]

    def __init__(self, work, **kwargs):
        """ Define Settings object """
        #
        # defining_actions
        # defined_actions
        # settings          Setting-obj
        #
        kwargs["name"] = mc.SETTINGS
        super().__init__(work, **kwargs)

        # Update fields that depend on settings (and NARRATOR)
        if self.work.defined_actions.get(mc.NARRATOR, None) is not None:
            # Update NARRATOR
            narrator = self.work.defined_actions[mc.NARRATOR]
            narrator.lang = self.default_lang
            # Update NARRATOR dependent actions's fields
            for paragraph in self.work.paragraphs:
                for key, value in self.work.defaults.items():
                    setattr(paragraph, key, getattr(narrator, key, value))

        self.work.settings = self
        super().define_action()
        #message(self.work, "SE0010")

    def do(self, *args, **kwargs):
        """ Settings DO NOT return audio """
        return None

