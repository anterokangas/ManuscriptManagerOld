"""
Manuscript Manger
The main program
"""

from manuscript.elements.work import Work

#from manuscript.elements.wait import Wait
#from manuscript.elements.settings import Group

from manuscript.messages.messages import message

from manuscript.tools.box_text import box_text

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

    manuscript = """
    (SETTINGS General
        (default_lang fi)
        (* mp3 settings *)
        (export testi.mp3)
        (format mp3)
        (title MM-kielen testi)
        (artist Various Artists)
        (album MM-single number 1)
        (comments The best Test-file ever!)
        (date 2019)
        (genre pop)
        (play_final True)
        (print_text True)
        (print_defined_actions True)
        (print_manuscript True)
        (print_executions False)
        (play_while True)
    )
    (##################
    (SETTINGS mp3 (x x))
    (SETTINGS text_processing (x x))
    (SETTINGS debug (x x))
    #############)
    Tervepä terve!

    (ROLE A (speed 0.9))
    (A Missä kisu?)
    
    Tule tule, kiss, kiss.
    (A No siellähän sinä olet.)
    """

    print("Manuscript file read in")

    work = Work(manuscript)

    # if drama.settings.export:
    #     drama.export()
    #     print(f"Drama exported as {Definition.settings.export}")

    if work.settings.print_manuscript:
        print("Parse manuscript:")
        for i, (command, action, params) in enumerate(work.parsed_manuscript):
            print(f"{i:4}: {command}, {action}, {params}")

    if work.settings.play_final:
        message("ME0010")
        print("Defined actions:")
        for key, value in work.defined_actions.items():
            print(f"===> defined action {key}={value}")
        work.play()

    print("\nREADY.")
