
if __name__ == "__main__":
    """ Manuscript manager
    1. create lexical analyser and parser
    2. define actors NARRATOR and BREAK
    3. parse manuscript and create list of actions
    4. make mp3 file
    5. play result file
    """
    #global playlist
    print(box_text(
        [
            "Manuscript Manager",
            "==================",
            "30.4.2019 (c) Antero Kangas",
            "",
            "Manuscript to mp3 file:",
            "+-------+    +----+    +-----+    +------+    +----+",
            "|MM-file| -> |read| -> |parse| -> |create| -> |play|",
            "+-------+    +----+    +-----+    +------+    +----+"
        ]
    ))
    lexer = ManuscriptLexer()
    parser = ManuscriptParser()
    # ----------------------------------
    # Default actors and actions
    # ----------------------------------
    defined_actions[NARRATOR] = Role(name=NARRATOR, lang='en')
    settings = Settings()   #  Default settings
    defined_actions[BREAK] = Wait(name=BREAK)
    manuscript += [
        (ROLE, Role, {'name': NARRATOR}),
        (WAIT, Wait, {'name': BREAK})
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

    if settings.print_text:
        lprint("Text", text.splitlines())

    if settings.print_defined_actions:
        print("Defined actions:")
        for name, action in defined_actions.items():
            print(f"\n{name} {type(action)}")
            length = max([len(value) for value in action.__dict__]) + 1
            for key, value in action.__dict__.items():
                if key != 'params':
                    print(f"   {key:{length}} {value}")
        lprint("Defined actions", defined_actions)

    if settings.print_manuscript:
        lprint(" Manuscript", manuscript)

    print("Create play")
    create_playlist(manuscript)

    playlist.export(
        settings.export,
        format=settings.format,
        tags={"title": settings.title,
              'artist': settings.artist,
              'album': settings.album,
              'comments': settings.comments,
              },
        cover=settings.cover,
    )
    print(f"Playlist saved as {settings.export}")

    if settings.play_final:
        time.sleep(5)
        print(f"Play result")
        playsound(settings.export)

    print("READY.")