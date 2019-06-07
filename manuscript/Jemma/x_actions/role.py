import copy
from manuscript.actions.definition import Definition
from manuscript.actions.sound import create_sound
import manuscript.tools.constants as mc
from manuscript.tools.process_sound import speak
from manuscript.tools.castings import bool_


class Role(Definition):
    """ Definition of Role object and dialogue """
    # _params[required, optional, dependent]
    # (attribute name, type conversion function, default value)
    params = [
        {},
        {"pitch": (float, 0.0),
         "speed": (float, 0.0),
         "gain": (float, 1.0),
         "noname": (bool_, False),        # name is never spoken
         "like": (str, mc.NARRATOR),     # speak as 'like' except lang, default text == alias
         mc.SOUND: (str, None)},         # generate SOUND object
        {"alias": (str, "name"),         # default value == dependent on
         "lang": (str, "default_lang")}  # look first self, then settings
    ]

    def __init__(self, **kwargs):
        """ define Role object """
        print(f"\nRole __init__ ()")
        for key, value in kwargs.items():
            print(f">{key} = {value}")
        super().__init__(**kwargs)

    def speak(self, text_):
        """ Convert text to AudioSegment (sound) object"""
        if re.sub('[(){}<> .!?,;]', '', text_) == "":
            # Nothing to say!
            return

        tts = gTTS(text=text_,
                   lang=self.lang)

        tf = NamedTemporaryFile(delete=False)
        tmp_file = tf.name
        tts.save(tmp_file)
        sound = AudioSegment.from_mp3(tmp_file)
        sound = speed_change(sound, self.speed)
        sound = pitch_change(sound, self.pitch)

        if Definition.settings.play_while:
            with Counter(prefix) as counter:
                tmp_file = prefix + f"_{counter:04d}.mp3"
                sound.export(tmp_file)

            playsound(tmp_file)
            os.remove(tmp_file)

        return sound

    def do(self, **kwargs):
        """
        Do Role object call
        :param kwargs: overriding parameterss
        :return: None
        """
        print(f"\nRole do()")
        for key, value in kwargs.items():
            print(f">{key} = {value}")
        text_ = kwargs.pop(mc.VALUES, "")
        sound_name = kwargs.get(mc.SOUND, None)
        if text_ == "":
            text_ = self.alias
            kwargs[mc.VALUES] = text_
            like = kwargs.get('like', mc.NARRATOR)
            # object 'like' is taken in to account
            # ONLY IF speaking alias name == no initial text
            try:
                # First use "like"'s parameters
                me = copy.deepcopy(Definition.defined_actions[like])
                like_kwargs = me.__dict__
                # Always override "lang" by original's (==self)
                like_kwargs['lang'] = self.lang
                # Then use all new parameters to override
                for kwarg in kwargs:
                    like_kwargs[kwarg] = kwargs[kwarg]
                # This time no object is going to be overriddden
                # "name" == None signals this to superclass's do
                like_kwargs["name"] = None
                kwargs = like_kwargs
                # Execute super class's do to convert values
                me = Definition.do(me, **kwargs)
            except Exception as e:
                raise ValueError(f"*** Undefined like='{like}': {e}")
        else:
            me = super().do(**kwargs)
        sound = speak(text_, create_sound=sound_name, **me.__dict__)
        if sound_name is None:
            return me  #  if no sound then return the Role object
        if sound_name in Definition.defined_actions.keys():
            raise ValueError(
                f" *** Line {p.lineno}: Double {sound_name} definition")

        kwargs = {key: kwargs[key] for key in
                  set(kwargs.keys()).intersection(
                      set(Sound.__dict__.keys()))}
        kwargs["audio"] = sound
        return create_sound(sound_name, **kwargs)
        # object_ = DEFINING_ACTIONS[SOUND](
        #     name=sound_name, __VALUES__=add_quotes(sound_name), **kwargs)
        # defined_actions[sound_name] = object_
        #
        # return sound_name,\
        #        object_,\
        #        {"name": sound_name, VALUES: sound_name, **kwargs}


# --------------------------------------------------
# Add the class to defined actions
# --------------------------------------------------
Definition.defining_actions[mc.ROLE] = Role

