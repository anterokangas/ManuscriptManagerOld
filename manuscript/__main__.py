"""
Manscript Manger
The main program
"""
import os

from manuscript.language.lexer import ManuscriptLexer
from manuscript.language.parser import ManuscriptParser
import manuscript.language.constants as mc

from manuscript.elements.definition import Definition
from manuscript.elements.role import Role
#from manuscript.elements.wait import Wait
from manuscript.elements.settings import Settings
from manuscript.elements.playlist import Playlist

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
    # Notice! 'lang' must be given if defined before Settings
    Definition.defined_actions[mc.NARRATOR] = Role(name=mc.NARRATOR, lang='en')
    Definition.settings = Settings()
    #Definition.defined_actions[mc.BREAK] = Wait(name=mc.BREAK)
    # The default 'Settings' is not added to structured manuscript
    manuscript = [
    #    (mc.ROLE, Definition.defined_actions[mc.NARRATOR], {'name': mc.NARRATOR}),
    #    (mc.WAIT, Definition.defined_actions[mc.WAIT], {'name': mc.BREAK})
    ]

    #cwd = os.getcwd()
    #files = os.listdir()
    #with open("testi.txt", "rb") as file:
    #    text = file.read().decode("UTF-8")

    text = """
    (SETTINGS
        (print_text True)
        (print_defined_actions True)
        (print_manuscript True)
        (print_executions True)
        (play_while True)
    )
    (SOUND NAUKAISU (input meow.mp3)) 
    (NARRATOR Narrator (SOUND KERTOJA) (lang en))
    
    Nyt puhuu kertoja eli NARRATORI
    (ROLE A (lang fi))
    (A Terve)
    """

    print("Manuscript file read in")
    pp = parser.parse(lexer.tokenize(text))
    if pp is not None:
        manuscript += pp
    print(f"Manuscript file parsed {len(manuscript)}")

    if Definition.settings.print_text:
        print_list("Text", text.splitlines())

    if Definition.settings.print_defined_actions:
        print(f"Defined actions {len(Definition.defined_actions)}:")
        for name, action in Definition.defined_actions.items():
            print(f"\n{name} {type(action)}")
            length = max([len(value) for value in action.__dict__]) + 1
            for key, value in action.__dict__.items():
                if key != 'params':
                    print(f"   {key:{length}} {value}")
        print_list("Defined actions", Definition.defined_actions)

    if Definition.settings.print_manuscript:
        print_list(" Manuscript", manuscript)

    the_play = Playlist(manuscript)

    print_list("Re-defined actions", Definition.defined_actions)

    the_play.export()
    print(f"Playlist exported as {Definition.settings.export}")

    if Definition.settings.play_final:
        the_play.play()

    print("READY.")