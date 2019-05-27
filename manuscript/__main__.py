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
        +-------+    +----+    +-----+    +------+    +----+
        |MM-file| -> |read| -> |parse| -> |create| -> |play|
        +-------+    +----+    +-----+    +------+    +----+
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
        (print_defined_actions True)
        (print_manuscript True)
        (print_executions True)
        (play_while False)
    )
    (# ---------------------------- #)
    Tästä se lähtee
    (ROLE B C)
    (ROLE A)
    (A 1 (SOUND 1))
    (1 (gain 1))
    (A 2 (SOUND 2))
    (SOUND 12 (input 1 2 meow.mp3))
    Eka (12)
    Toka (yxkax)
    (1 (input 2))
    @
    (0 1 2) - no
    (1 2) - play 1 2
    (1 2 (SOUND yxkax)) -> create yxkax == 1 2
    (SOUND 12 (input 1 2)) -> create 12 = 1 2
    (1 (input 2)) -> play 1 2
    (1  (input 2) (SOUND 12)) -> create 12
    
    I PHASE (parse)
    1. (def name values [params]) -> if allowed(name) and values != "" 
                                  -> create def-object(name=name, params=values&params)
    2. (defined [params]) -> defined.do(params)
    3. (defined values [params]) if defined is not SOUND -> defined.do(values, params)
                                 if defined is SOUND 
                                    -> create SOUND-object(name=tmp, 
                                                           input=defined&values, 
                                                           params)
    4. (nondefined [values] [params]) -> create SOUND-object(name=tmp, input=nondefined&values, params); tmp.do()
    5. (nondefining [values] [params](SOUND=sound_name)) -> if allowed(sound_name)
                                                    ->create SOUND-object(name=sound_name,
                                                                          input=nondefining&values
                                                                          params9
     
     """
    print("Manuscript file read in")

    work = Work(manuscript_text)
    len_audio = len(work.audio) if work.audio is not None else 0

    if work.settings.print_manuscript:
        print("Parsed manuscript:")
        for i, (command, action, params) in enumerate(work.parsed_manuscript):
            print(f"{i:4}: {command}, {action}, {params}")

    if work.settings.print_defined_actions:
        print("Defined actions")
        print( work.defined_actions)
        for action, parameters in work.defined_actions.items():
            print(f"   {action}")
            for key, value in parameters.__dict__.items():
                print(f"      {key:15}: {value}")
                if key != "audio":
                    continue
                length = len(value) if value is not None else 0
                print(f"      - audio_length : {length}")

    if work.settings.export:
        work.export_audio()
        print(f"Work exported as {work.settings.export}")

    print(f"work.settings.play_final={work.settings.play_final}")
    if work.settings.play_final:
        message(work, "ME0010")
        work.play()

    print(f"\nAudio generated, length={len_audio}.")