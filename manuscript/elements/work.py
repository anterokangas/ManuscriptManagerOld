from tqdm import tqdm
import copy

from manuscript.elements.definition import Definition
from manuscript.elements.role import Role
from manuscript.elements.wait import Wait
from manuscript.elements.sound import Sound
#from manuscript.elements.settings import Group
from manuscript.elements.settings import Settings

from manuscript.language.lexer import ManuscriptLexer
from manuscript.language.parser import ManuscriptParser

from manuscript.messages.messages import message_text

import manuscript.tools.audio as audio
import manuscript.tools.constants as mc
import manuscript.tools.play as play

from manuscript.tools.subclasses import get_all_subclasses


class Work:
    """
    Work - class as a namespace.


    Class attributes
    ----------------
    defining_actions :  dictionary of form {NAME: NameClass, ...}
        Collection of classes that define Actions

    defined_action :    dictionary of form {NAME: object.do(), ...}
        Collection of defined action objects

    manuscript :        list of

    Class methods
    -------------
    """

    def __init__(self, manuscript):
        """ Initialize and make a new work

        (1) Define defining actions
        (2) Initialize default defined actions
        (3) Create lexer and parser
        (4) Make lexical analysis and parse manuscript
        (5) create audio
        """
        self.manuscript_text = manuscript

        # The defining actions are subclassess of Definition having COMMAND
        self.defining_actions = {}
        for subclass in get_all_subclasses(Definition):
            if 'COMMAND' in subclass.__dict__.keys():
                self.defining_actions[subclass.COMMAND] = subclass

        # Names whose re-definition is allowed
        self.re_definition_allowed = {mc.SETTINGS}

        # Initialize default defined actions
        self.defined_actions = {}
        self.settings = Settings(self)
        Role(self, name=mc.NARRATOR)
        Wait(self, name=mc.BREAK)

        # Make lexer and parser
        lexer = ManuscriptLexer()
        parser = ManuscriptParser(work=self)
        # Make lexical analysisis and parse manuscript
        self.parsed_manuscript = parser.parse(lexer.tokenize(manuscript))

        print("\nWork: defining actions")
        for key, value in self.defining_actions.items():
            print(f"   {key:15}: {value}")

        print("\nWork: parsed_manusript")
        for act in self.parsed_manuscript:
            print(f"   {act}")

        print("\nWork: defined actions")
        for key, value in self.defined_actions.items():
            if isinstance(value, Sound):
                audio_length = len(value.audio) if value.audio is not None else 0
            else:
                audio_length = ""

            print(f"   {key:15}: {value} {audio_length}")

        # Make audio
        self.audio = self._process_structured_manuscript()

    def define_action(self, action_name, object_):
        """ Add new defined action """
        self.defined_actions[action_name] = object_

    def export_audio(self):
        print(f"Work.export_audio: {self.settings.export}")
        if self.audio is None:
            print(f"Empty audio")
            return
        self.audio.export(self.settings.export)

    def _process_structured_manuscript(self):
        """ Process structured manuscript and create audio """
        the_audio = None

        # Execute defined actions
        for i, (command, action, params) in tqdm(enumerate(self.parsed_manuscript)):

            # If asked print current action
            if self.settings.print_executions:
                print(f"\n{i}: {command}, {action}, {params}")

            if command in self.defining_actions:
                print(f"Command {command} is a defining action")
                continue

            print(f"defined_actions {self.defined_actions.keys()}")
            if command not in self.defined_actions:
                print(f"*** Error: {command} is not defined")
                continue

            print(f"command {command} is Ok, action={action}")
            if action is None:
                action = self.defined_actions[command]

            print(f"action={action}")
            sound = action.do(**params)
            length = len(sound) if sound is not None else 0
            print(f"-->sound={sound} {length}")
            the_audio = audio.append(the_audio, sound)
            length = len(the_audio) if the_audio is not None else 0
            print(f"+----> the_audio={the_audio} {length}")
        print(f"===========> the_audio={the_audio} {length}")
        return the_audio

    def definition_allowed(self, name):
        """  Decides can 'name' be defined or re-defined  """
        return name != "" and \
            (name not in set(self.defined_actions.keys())
             or name in self.re_definition_allowed)

    def play(self):
        play.play(self.audio, block=False)

    def to_formatted_text(self):
        # TODO: Create readable formatted manuscript
        pass
