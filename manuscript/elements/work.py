from tqdm import tqdm
import copy

from manuscript.elements.definition import Definition
from manuscript.elements.role import Role
from manuscript.elements.wait import Wait
#from manuscript.elements.settings import Group
from manuscript.elements.settings import Settings

from manuscript.language.lexer import ManuscriptLexer
from manuscript.language.parser import ManuscriptParser

from manuscript.messages.messages import message_text

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
        self.define_action(mc.NARRATOR, Role(self, name=mc.NARRATOR, lang='en'))
        self.settings = Settings(self)
        # self.define_action(mc.SETTINGS, Settings(self))
        self.define_action(mc.BREAK, Wait(self, name=mc.BREAK, time='0.3'))
        # self.settings = self.defined_actions[mc.SETTINGS]

        print(f"defining_actions {len(self.defining_actions)} =\n{self.defining_actions}")
        print(f"defined_actions {len(self.defined_actions)} =\n{self.defined_actions}")

        # Make lexer and parser
        lexer = ManuscriptLexer()
        parser = ManuscriptParser(work=self)
        # Make lexical analysisis and parse manuscript
        self.parsed_manuscript = parser.parse(lexer.tokenize(manuscript))
        print("Work: parsed_manusript")
        for act in self.parsed_manuscript:
            print(f"   {act}")

        # Make audio
        self.audio = self._process_structured_manuscript()

    def define_action(self, action_name, object_):
        """ Add new defined action """
        print(f"define action {action_name} {object_}")
        self.defined_actions[action_name] = object_

    def _append_audio(self, audio):
        if audio is None:
            try:
                print(audio)
            except Exception as e:
                self.audio = None
            return
        if self.audio is None:
            self.audio = audio
        else:
            self.audio.append(audio)

    def export_audio(self):
        print(f"Work.export_audio: {self.settings.export}")
        self.audio.export(self.settings.export)

    def _process_structured_manuscript(self):
        """ Process structured manuscript and create audio """
        the_audio = None

        print(f"1type((the_audio)={type(the_audio)}")

        # Execute defined actions
        for i, (command, action, params) in tqdm(enumerate(self.parsed_manuscript)):

            # If asked print current action
            if self.settings.print_executions:
                print(f"\n{i}: {command}, {action}, {params}")
                if the_audio is not None:
                    print(type(the_audio), len(the_audio))
                for key, value in self.defined_actions.items():
                    print(f"---> defined action {key}={value}")

            # If action is not defined then the command is a defining action
            # ==> get the corresponding defining action
            if action is None:
                # Lazy evaluation (e.g. ROLE --> SOUND)
                # print(f"Lazy evaluation command={command}")
                action = self.defined_actions.get(command, None)
                if action is None:
                    raise ValueError(self, message_text(self, "PL8010")[0].format(command))

            name = params.get("name", "")
            # print(type(action))
            if isinstance(action, Definition):
                # action of a defined action --> makes audio
                audio = action.do(**params)
                print(f"action.do()-> audio, the_audio={type(audio)}, {type(the_audio)}")
                print(f"2type((the_audio)={type(the_audio)}")
                if audio is not None:
                    if the_audio is None:
                        the_audio = copy.copy(audio)
                        print(f"type3((the_audio)={type(the_audio)}")
                    else:
                        print(type(audio), type(the_audio))
                        the_audio = the_audio.append(audio)
                        print(f"type3((the_audio)={type(the_audio)}")
                # print(type(the_audio), len(the_audio))
            elif self.definition_allowed(name):
                # Definition of new action object -> defines a new object
                object_ = action(self, **params)
                self.define_action(object_.name, object_)
            else:
                print(f"Work: create_audio -->{name} was already defined")
                pass
        return the_audio

    def definition_allowed(self, name):
        """  Decides can 'name' be defined or re-defined  """
        return name not in set(self.defined_actions.keys()) \
            or name in self.re_definition_allowed \
            or name[0] == "_"

    def play(self):
        play.play(self.audio, block=False)

    def to_formatted_text(self):
        # TODO: Create readable formatted manuscript
        pass
