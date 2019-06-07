"""
Manuscript Manger
The main program
"""
import sys

import colorama
from termcolor import colored

from manuscript.elements.work import Work
import manuscript.exceptions.exceptions as mex
from manuscript.tools.castings import supported_languages
import manuscript.tools.play as play
from manuscript.tools.box_text import box_text


if __name__ == "__main__":
    """ Manuscript manager
    1. create lexical analyser and parser
    2. define actors NARRATOR and BREAK
    3. parse manuscript and create list of actions
    4. make mp3 file
    5. play result file
    """
    colorama.init()
    print(box_text("""
        Manuscript Manager
        ==================
        Version 0.01 8.5.2019 (c) Antero Kangas
        Version 0.02 28.5.2019 (c) Antero Kangas
        
        Manuscript to mp3 file:
        (         )    +----+    +-----+    +------+    ( mp3-> play )
        ( MM-file ) -> |read| -> |parse| -> |create| -> ( text       )
        (         )    +----+    +-----+    +------+    ( word?      ) 
        """
                   ))

    print(f"{'Read manuscript'}")
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
        (print_supported_languages False)
        (print_defining_actions False)
        (print_defined_actions True)
        (print_manuscript_text False)
        (print_manuscript_parsed False)
        (print_executions False)
        (play_while False)
    )
    (# ---------------------------- #)
    (title Löikö Mörkö sisään?)
    (ROLE A (speed 0.99))
    (ROLE B (speed 1.01) (gain 10))
    (ROLE C (speed 1) (pitch 0.9))
    
    (A A Mörkö, mörkö!)
    (B B Mörkö, mörkö!)
    (C C Mörkö, mörkö!)
    
    Tavataanko Kankkulan kaivolla?
    (BREAK)
    Ei toki, vaan torilla, Keskustorilla, nääs!
    """
    try:
        work = Work(manuscript_text)

        len_audio = len(work.audio) if work.audio is not None else 0
        print(f"\nAudio generated, length={len_audio/1000.0} seconds.")

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

        if work.settings.print_supported_languages:
            print(f"\n{supported_languages()}")

        if work.settings.export:
            work.export_audio()
            print(f"\nWork exported as {work.settings.export}")

        if work.settings.play_final:
            #message(work, "ME0010")
            print("Play audio")
            play.play_sound(work.audio, block=True)

            from playsound import playsound
            playsound("data//Kling.mp3", block=False)

        print("READY.")


    except (mex.MMSyntaxError,
            mex.MMValueError,
            mex.MMParameterError) as exception_text:
        print(colored("\n" + str(exception_text), 'red'))
        sys.exit(1)
