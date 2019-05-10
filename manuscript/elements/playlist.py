from tqdm import tqdm
from manuscript.elements.definition import Definition
import manuscript.language.constants as mc


class Playlist:

    def __init__(self, the_manuscript):
        """
        (ROLE A) --> new object Role.A
        (A text) --> A.do(text) == speak
        (A)      --> A.do(A.alias) == speak
        (A text (SOUND B)) new object Sound.B (audio=(A text))
        (A (SOUND B)) new object Sound.B (audio=(A A.alias9
        :param the_manuscript:
        :return:
        """
        self.playlist = None
        i = 0
        for command, action, params in tqdm(the_manuscript):
            if Definition.settings.print_executions:
                print(f"\n{i} {command} {type(command)} {params}")
            i += 1
            if action is None:
                # Lazy evaluation (e.g. ROLE --> SOUND)
                print(f"Lazy evaluation command={command}")
                action = Definition.defined_actions[command]

            name = params.get("name", "")
            if isinstance(action, Definition):
                # action of defined action
                print(f"Do object command={command}")
                sound = action.do(**params)
                self.append(sound)
            elif name not in Definition.defined_actions:
                # Definition of new action object
                print(f"Create object command={command}")
                object_ = action(**params)
                print(f"-->add {object_.name} {name}")
                Definition.defined_actions[object_.name] = object_
            else:
                print(f"-->{name} was already defined")

    def append(self, sound):
        if self.playlist is None:
            self.playlist = sound
        else:
            self.playlist += sound

    def play(self):
        print(f"play playlist {len(self.playlist)}")
        pass

    def export(self):
        self.playlist.export(
            Definition.settings.export,
            format=Definition.settings.format,
            tags={"title": Definition.settings.title,
                  'artist': Definition.settings.artist,
                  'album': Definition.settings.album,
                  'comments': Definition.settings.comments,
                  },
            cover=Definition.settings.cover,
        )
