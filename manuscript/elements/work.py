from tqdm import tqdm
import pydub.playback as playback

from manuscript.elements.definition import Definition
from manuscript.elements.role import Role
#from manuscript.elements.settings import Group
from manuscript.elements.settings import Settings

from manuscript.language.lexer import ManuscriptLexer
from manuscript.language.parser import ManuscriptParser
import manuscript.tools.constants as mc

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
        print(manuscript)
        Definition.producer = self          # The place where settings are
        #Settings.producer = self           # The place where settings are
        self.settings = Settings()          # Initialize by using the default settings
        # self.defining_actions = {
        #     mc.ROLE: Role,
        #     mc.SOUND: Sound,
        #     mc.WAIT: Wait,
        #     # TODO: mc.GROUP: Group,
        #     mc.SETTINGS: Settings,
        # }
        self.defining_actions = {}
        for subclass in get_all_subclasses(Definition):
            if 'COMMAND' in subclass.__dict__.keys():
                self.defining_actions[subclass.COMMAND] = subclass

        self.defined_actions = {}
        # Define default objects (command_name, object_)
        self.define_action(mc.NARRATOR, Role(name=mc.NARRATOR, lang='en'))
        #self.add_defined_action(mc.BREAK, Wait(name=mc.BREAK, time='0.3'))

        print(f"defining_actions {len(self.defining_actions)}=\n{self.defining_actions}")
        print(f"defined_actions {len(self.defined_actions)}=\n{self.defined_actions}")

        print(20*"-")
        lexer = ManuscriptLexer()
        parser = ManuscriptParser(producer=self)
        self.parsed_manuscript = parser.parse(lexer.tokenize(manuscript))
        self.sound = self._create_sound()

    def define_action(self, action_name, object_):
        self.defined_actions[action_name] = object_

    def append_sound(self, sound):
        if sound is None:
            return
        if self.sound is None:
            self.sound = sound
        else:
            self.sound.append(sound)

    def export_sound(self):
        self.sound.export(self.settings.export)

    def _create_sound(self):
        """ Process structured manuscript and create sound """
        the_sound = None
        i = 0
        for command, action, params in tqdm(self.parsed_manuscript):
            if self.settings.print_executions:
                print(f"\n{i}: {command}, {action}, {params}")
                print(self.settings.print_executions)
                if the_sound is not None:
                    print(len(the_sound))
                for key, value in self.defined_actions.items():
                    print(f"---> defined action {key}={value}")
            i += 1

            if action is None:
                # Lazy evaluation (e.g. ROLE --> SOUND)
                #print(f"Lazy evaluation command={command}")
                action = self.defining_actions.get(command, None)
                if action is None:
                    raise ValueError(message_text("PL8010")[0].format(command))

            name = params.get("name", "")
            # print(type(action))
            if isinstance(action, Definition):
                # action of a defined action --> makes sound
                #print(f"Do object command={command}")
                sound = action.do(**params)
                #print(type(sound), len(sound))
                if sound is not None:
                    if the_sound is None:
                        the_sound = sound
                    else:
                        the_sound = the_sound.append(sound)
                # print(type(the_sound), len(the_sound))
            elif name not in self.defined_actions:
                # Definition of new action object -> defines a new object
                #print(f"Create object command={command}")
                object_ = action(**params)
                self.define_action(object_.name, object_)
            else:
                #print(f"-->{name} was already defined")
                pass
        return the_sound

    def play(self):
        if self.sound is not None:
            print(f"length of final sound={len(self.sound)}")
            playback.play(self.sound)


    def to_formatted_text(self):
        # TODO: Create readable formatted manuscript
        pass
