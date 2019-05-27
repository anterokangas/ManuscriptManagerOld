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
        (* --- finals --- *)
        (play_final True)
        (print_final_text True)
        (* --- DEBUG settings --- *)
        (print_defining_actions True)
        (print_defined_actions True)
        (print_manuscript_text True)
        (print_manuscript_parsed False)
        (print_executions True)
        (play_while False)
    )
    (# ---------------------------- #)
    (ROLE A (speed 0.99))
    (ROLE B (speed 1.01))
    (ROLE C (speed 1) (pitch 0.9))
   
    (A Eläköön! (SOUND AA))
    (B Eläköön! (SOUND BB))
    (C Eläköön! (SOUND CC))
    (SOUND RC (input CC) (reverse True) (speed -1))
    (RC)
    (BREAK (delay 5))
    (#(AA BB CC (overlay True))
    #)
    (GROUP ABC (members A B C))
    (ABC Eläköön! Eläköön! Eläköön!)
    
    
     """
    print("\nManuscript file read in")

    work = Work(manuscript_text)
    len_audio = len(work.audio) if work.audio is not None else 0

    if work.settings.print_manuscript_parsed:
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

        for action, object_ in work.defined_actions.items():
            try:
                length = len(object_.audio)
            except:
                length = ""
            print(f"   {action:15}: {type(object_)} {length}")

    if work.settings.export:
        work.export_audio()
        print(f"\nWork exported as {work.settings.export}")

    print(f"work.settings.play_final={work.settings.play_final}")
    if work.settings.play_final:
        message(work, "ME0010")
        work.play()

    print(f"\nAudio generated, length={len_audio}.")