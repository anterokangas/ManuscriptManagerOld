"""
Manuscript Manger
The main program
"""

from manuscript.elements.work import Work

from manuscript.messages.messages import message
from manuscript.tools.play import play
from playsound import playsound
from manuscript.tools.box_text import box_text
import time


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
        *---------*    +----+    +-----+    +------+    | mp3-> play |
        | MM-file | -> |read| -> |parse| -> |create| -> | text       |
        *---------*    +----+    +-----+    +------+    | word?      | 
        """
                   ))

    manuscript_text = """
    (# ---------------------------- #)
    (SETTINGS General
        (default_lang fi)
        (* --- mp3 settings --- *)
        (export testi.mp3)
        (format mp3)
        (title MM-kielen testi)
        (artist Various Artists)
        (album MM-single number 1)
        (comments The best Test-file ever!)
        (date 2019)
        (genre pop)
        (* --- DEBUG settings --- *)
        (play_final True)
        (print_text True)
        (print_defined_actions False)
        (print_manuscript False)
        (print_executions False)
        (play_while False)
    )
    (# ---------------------------- #)
    5 (BREAK( delay 5))
    
    4 (BREAK( delay 4))
    3 (BREAK( delay 3))
    2 (BREAK( delay 1))
    1 (BREAK( delay 1))
    0 (BREAK)
    0 0 0 0 
    0
    
    (ROLE A)
    (A Hei 1)
    (A Hei 2 (speed -1))
    (A Hei 3)
    (meow.mp3 meow.mp3(SOUND MEOW))
    2 2 naukaisua
    (MEOW)tauko(MEOW) 
    Uusiksi, välissä tauko.
    (WAIT Pitkä_tauko (delay 10))
    (MEOW)(BREAK (delay 5))(MEOW) 
    ja vielä tuplatupla
    (MEOW Pitkä_tauko MEOW)  
     """
    print("\nManuscript file read in")

    work = Work(manuscript_text)
    len_audio = len(work.audio) if work.audio is not None else 0

    if work.settings.print_manuscript:
        print("\nParsed manuscript:")
        for i, (command, action, params) in enumerate(work.parsed_manuscript):
            print(f"{i:4}: {command}, {action}, {params}")

    if work.settings.print_defined_actions:
        print("\nDefined actions")
        print( work.defined_actions)
        for action, object_ in work.defined_actions.items():
            print(f"   {action}      {object_}")
            for key, value in object_.__dict__.items():
                print(f"      {key:15}: {value}")
                if key != "audio":
                    continue
                length = len(value) if value is not None else 0
                print(f"      - audio_length : {length}")

    if work.settings.export:
        work.export_audio()
        print(f"\nWork exported as {work.settings.export}")

    print(f"work.settings.play_final={work.settings.play_final}")
    if work.settings.play_final:
        message(work, "ME0010")
        work.play()

    print(f"\nAudio generated, length={len_audio}.")