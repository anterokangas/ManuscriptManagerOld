from tqdm import tqdm
import copy

from manuscript.elements.definition import Definition
from manuscript.elements.role import Role
from manuscript.elements.wait import Wait
from manuscript.elements.sound import Sound
from manuscript.elements.group import Group
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

        print(f"{'Parse manuscript'}")
        self.parsed_manuscript = parser.parse(lexer.tokenize(manuscript))
        if self.settings.print_defining_actions:
            print("\nWork: defining actions")
            for key, value in self.defining_actions.items():
                print(f"   {key:15}: {value}")

        if self.settings.print_manuscript_parsed:
            print("\nWork: parsed_manuscript")
            for act in self.parsed_manuscript:
                print(f"   {act}")

        if self.settings.print_defined_actions:
            print("\nWork: defined actions")
            for key, value in self.defined_actions.items():
                if isinstance(value, Sound):
                    audio_length = len(value.audio) if value.audio is not None else 0
                    input_ = value.input
                else:
                    audio_length = ""
                    input_ = ""

                print(f"   {key:15}: {value} {audio_length} {input_}")

        # Make audio
        print(f"{'Process manuscript'}")
        self.audio = self._process_structured_manuscript()

    def define_action(self, action_name, object_):
        """ Add new defined action """
        self.defined_actions[action_name] = object_

    def export_audio(self):
        if self.audio is None:
            print(f"Empty audio")
            return
        self.audio.export(self.settings.export)

    def _process_structured_manuscript(self):
        """ Process structured manuscript and create audio """
        the_audio = None

        # Execute defined actions
        i = 0
        for command, action, params in tqdm(self.parsed_manuscript):

            # If asked print current action
            if self.settings.print_executions:
                print(f"\n{i}: {command}, {action}, {params}")
            i += 1
            if command in self.defining_actions:
                continue

            if command not in self.defined_actions:
                continue

            if action is None:
                action = self.defined_actions[command]
            sound = action.do(**params)
            if params.get(mc.SOUND, "") == "":
                the_audio = audio.append(the_audio, sound)
        return the_audio

    def definition_allowed(self, name):
        """  Decides can 'name' be defined or re-defined  """
        return (name != ""
                    and name not in self.defining_actions.keys()
                    and name not in self.defined_actions.keys()
                or name in self.re_definition_allowed)

    def play(self):
        print(f"work play {self.audio} {len(self.audio)}")
        play.play_sound(self.audio)

    def to_formatted_text(self):
        # TODO: Create readable formatted manuscript
        pass
