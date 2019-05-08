"""
Manscript Manger
The main program
"""
import os

from manuscript.language.lexer import ManuscriptLexer
from manuscript.language.parser import ManuscriptParser
import manuscript.language.constants as mc
from manuscript.actions.definition import Definition
from manuscript.actions.role import Role
from manuscript.actions.wait import Wait
from manuscript.actions.settings import Settings
from manuscript.tools.box_text import box_text
from manuscript.tools.print_list import print_list


if __name__ == "__main__":
    """ Manuscript manager
    1. create lexical analyser and parser
    2. define actors NARRATOR and BREAK
    3. parse manuscript and create list of actions
    4. make mp3 file
    5. play result file
    """
    #global playlist
    print(box_text("""
        Manuscript Manager
        ==================
        8.5.2019 (c) Antero Kangas
        
        Manuscript to mp3 file:
        +-------+    +----+    +-----+    +------+    +----+
        |MM-file| -> |read| -> |parse| -> |create| -> |play|
        +-------+    +----+    +-----+    +------+    +----+
        """
    ))
    lexer = ManuscriptLexer()
    parser = ManuscriptParser()
    # ----------------------------------
    # Default actors and actions
    # ----------------------------------
    Definition.defined_actions[mc.NARRATOR] = Role(name=mc.NARRATOR, lang='en')
    Definition.settings = Settings()        #  Default settings
    Definition.defined_actions[mc.BREAK] = Wait(name=mc.BREAK)
    manuscript = [
        (mc.ROLE, {'name': mc.NARRATOR}),
        (mc.WAIT, {'name': mc.BREAK})
    ]

    cwd = os.getcwd()
    files = os.listdir()
    with open("testi.txt", "rb") as file:
        text = file.read().decode("UTF-8")

    print("Manuscript file read in")
    pp = parser.parse(lexer.tokenize(text))
    if pp is not None:
        manuscript += pp
    print("Manuscript file parsed")

    if Definition.settings.print_text:
        print_list("Text", text.splitlines())

    if Definition.settings.print_defined_actions:
        print("Defined actions:")
        for name, action in Definition.defined_actions.items():
            print(f"\n{name} {type(action)}")
            length = max([len(value) for value in action.__dict__]) + 1
            for key, value in action.__dict__.items():
                if key != 'params':
                    print(f"   {key:{length}} {value}")
        print_list("Defined actions", defined_actions)

    if Definition.settings.print_manuscript:
        print_list(" Manuscript", manuscript)

    print("Create play")
    create_playlist(manuscript)

    playlist.export(
        settings.export,
        format=Definition.settings.format,
        tags={"title": Definition.settings.title,
              'artist': Definition.settings.artist,
              'album': Definition.settings.album,
              'comments': Definition.settings.comments,
              },
        cover=Definition.settings.cover,
    )
    print(f"Playlist saved as {Definition.settings.export}")

    if Definition.settings.play_final:
        time.sleep(5)
        print(f"Play result")
        playsound(settings.export)

    print("READY.")