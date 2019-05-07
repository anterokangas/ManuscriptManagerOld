# -*- coding: utf-8 -*-

from gtts import gTTS
from playsound import playsound
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
import time
from tqdm import tqdm
import re
import sys
import os
import copy
from sly import Lexer, Parser
import shlex


"""
PyCharm

Parser
"""


COMMAND = "__COMMAND__"
COMMENT = "__COMMENT__"
VALUES = "__VALUES__"

NARRATOR = "NARRATOR"
BREAK = "BREAK"

ROLE = "ROLE"
SOUND = "SOUND"
GROUP = "GROUP"
WAIT = "WAIT"
SETTINGS = "SETTINGS"
DEBUG = "DEBUG"

EPSILON = sys.float_info.epsilon

#
# Globals
#
defined_actions = {}
manuscript = []
playlist = None  #  AudioSegment.empty()
narrator_speaking = False


class Counter:
    counters = {}

    def __init__(self, prefix):
        self.prefix = prefix
        if Counter.counters.get(self.prefix, 0) == 0:
            Counter.counters[self.prefix] = 0

    def __enter__(self):
        return Counter.counters[self.prefix]

    def __exit__(self, *args):
        Counter.counters[self.prefix] += 1


def debug(text_):
    """ Print text when DEBUG_ON is True """
    if DEBUG_ON:
        print(text_)


def speak(text_, create_sound=None, prefix="tmp", **kwargs):
    """ Convert text to AudioSegment (sound) object"""
    if re.sub('[(){}<> .!?,;]', '', text_) == "":
        # Nothing to say!
        return
    tts = gTTS(text=text_,
               lang=kwargs['lang'])
    #  with Counter(prefix) as counter:
    #    tmp_file = prefix + f"_{counter:04d}.mp3"
    #    tts.save(tmp_file)

    tf = NamedTemporaryFile(delete=False)
    tmp_file = tf.name
    tts.save(tmp_file)
    sound = AudioSegment.from_mp3(tmp_file)

    speed = kwargs['speed']
    sound = speed_change(sound, speed)

    pitch = kwargs['pitch']
    sound = pitch_change(sound, pitch)

    if create_sound is None:
        append_to_playlist(sound)

        if settings.play_while:
            with Counter(prefix) as counter:
                tmp_file = prefix + f"_{counter:04d}.mp3"
                sound.export(tmp_file)

            print(f"speak playwhile tmp_file={tmp_file}")

            playsound(tmp_file)
            os.remove(tmp_file)
    return sound



def append_to_playlist(sound):
    global playlist
    if playlist is None:
        playlist = sound
    else:
        playlist = playlist.append(sound)


def speed_change(sound, speed=0.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    speed = 1.0 + speed/10  # Tune speed value easier to use
    sound_with_altered_frame_rate = \
        sound._spawn(sound.raw_data,
                     overrides={"frame_rate": int(sound.frame_rate * speed)})
    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


def pitch_change(sound, pitch=0.0):
    pitch /= 10  #  Tune pitch value easier to use
    new_sample_rate = int(sound.frame_rate * (2.0 ** pitch))
    sound_with_altered_pitch = \
        sound._spawn(sound.raw_data,
                     overrides={'frame_rate': new_sample_rate})
    return sound_with_altered_pitch


def add_sound(filename, **kwargs):
    """ Play mp3 file """
    print(f"addsound {filename} {type(filename)}")
    if isinstance(filename, Sound):
        sound = filename.audio
    elif isinstance(filename, AudioSegment):
        sound = filename
    else:
        sound = AudioSegment.from_mp3(filename)
    append_to_playlist(sound)
    if settings.play_while and not isinstance(filename, AudioSegment):
        playsound(filename)


def add_silence(time):
    """ Create silence (time in seconds)"""
    silence = AudioSegment.silent(time*1000)
    append_to_playlist(silence)


def bool_(input_):
    """ Convert boolean or string to boolean, also 'False' and 'F' to False """
    return bool(input_) if input_.upper() not in ["FALSE", "F"] else False


def list_(input_):
    """ Convert sep-separated string to list """
    print(f"list_ input_={input_}")
    print(f"list_ output={shlex.split(input_, posix=False)}")
    return shlex.split(input_, posix=False)


def as_is(object_):
    return object_


def add_quotes(text_, always=False):
    if " " not in text_ and not always:
        # No need to add quotes
        return text_
    if '"' not in text_:
        return '"' + text_ + '"'
    if "'" not in text_:
        return "'" + text_ +"'"
    # Error
    raise ValueError(f"*** Cannot add quotes to string {text_}")


def remove_quotes(text_):
    if len(text_) <= 2:
        return text_
    if text_[0] == text[-1] == "'" \
       or text_[0] == text[-1] == '"':
        return text_[1:-1]
    return text_


def get_sound(sound_or_file):
    # sound_or_filesound_or_file is
    # either _ONE_ SOUND name or filename
    print(f"1get_sound {sound_or_file}")
    sound_or_file = remove_quotes(sound_or_file)
    print(f"2get_sound {sound_or_file}")
    sound_name = defined_actions.get(sound_or_file, None)
    if sound_name is None:
        for voice_directory in settings.voice_directories:
            try:
                sound = AudioSegment.from_mp3(
                    os.path.join(
                        voice_directory,
                        sound_or_file))
                return sound
            except:
                pass
        raise ValueError(f"*** No sound file {sound_or_file} found")
    else:
        sound = sound_name.audio
    return sound


class Definition:
    """ Super class for defining actions """
    params = [{"name": (str, None)}, #  Required (== not overriddable)
              {VALUES: (str, "")},   #  Optional
              {}]                    #  Dependent

    def __init__(self, **kwargs):
        """
        Initialize Manuscript Element Object
        ------------------------------------
        :param object: object to be initialized
        :param params: list of dicts of parameters: [required, optional, dependent]
                       each element of dict key {(convert_function, default_value)}
        :param kwargs: list of read parameters {key: value}
        :return: None
        """
        assert isinstance(self.params, list)
        assert len(self.params) == 3

        #
        # Complete params
        #
        self.params = [{**dp, **sp} for dp, sp in zip(Definition.params, self.params)]

        #
        # Set required parameters
        # Order: subclass's params can override superclass' params
        #
        for param, (func, default_value) in {**self.params[0], **Definition.params[0]}.items():
            val = kwargs.get(param, None)
            if val is not None:
                setattr(self, param, func(val))
            else:
                raise ValueError(f"*** Required parameter '{param}' missing")
            if param == 'input':
                print(
                    f"super__init0 after func {param} = {self.__dict__[param]}")

        #
        # Set optional parameters (default_value = name of the attribute)
        #
        for param, (func, default_value) in {**Definition.params[1], **self.params[1]}.items():
            val = kwargs.get(param, None)
            if val is not None:
                setattr(self, param, func(val))
            else:
                setattr(self, param, default_value)
            if param == 'input':
                print(
                    f"super__init1 after func {param} = {self.__dict__[param]}")
                print(f"That is {self.input}")
        #
        # set dependent parameters
        #
        # look
        #   1. kwargs == given parameters
        #   2. default value from self
        #   3. default value from settings
        #   4. otherwise --> error
        #
        for param, (func, default_value) in {**Definition.params[2], **self.params[2]}.items():
            val = kwargs.get(param, None)
            if val is None:
                val = kwargs.get(default_value, None)
            if val is None:
                val = settings.__dict__.get(default_value, None)
            if val is not None:
                setattr(self, param, func(val))
            else:
                raise ValueError(f"*** The parameter that {param} is dependent on is not set")
            if param == 'input':
                print(
                    f"super__init2 after func {param} = {self.__dict__[param]}")
        #
        # test if non-defined parameters
        #
        for kwarg in kwargs:
            if self.__dict__.get(kwarg, None) is None:
                raise ValueError(f"*** Non-defined parameter '{kwarg} = {kwargs[kwarg]}' in {self.__dict__}")

    def do(self, **kwargs):
        """
        Do defined action
        :param kwargs: Check and override parameters temporary
        :return: Overridden copy of object self
        """
        me = copy.deepcopy(self)
        for key, value in kwargs.items():
            if key == "params":
                continue
            if key not in vars(me):
                raise ValueError(f"*** {me.name} Trying to override non defined attribute '{key}'")
            # Required parameters == params[0] are not allowed to be overridden
            if key in self.params[0] and value != None:
                raise ValueError(f"*** {me.name} Trying to override required attribute '{key}'")
            #
            # Find conversion function and set attribute
            #
            func = self.params[0].get(key,
                       self.params[1].get(key,
                           self.params[2].get(key, ("", (str, "")))))[0]

            if key == VALUES:
                print(f"==>\nkey={key}\nvalue={value}\nfunc={func}\nfunc(value)={func(value)}")
            setattr(me, key, func(value))
        return me


class Role(Definition):
    """ Definition of Role object and dialogue """
    # params[required, optional, dependent]
    # (attribute name, type conversion function, default value)
    params = [
        {},
        {"pitch": (float, 0.0),
         "speed": (float, 0.0),
         "gain": (float, 1.0),
         "noname": (bool, False),   # name is never spoken
         "like": (str, NARRATOR),   # speak as 'like' except lang, default text == alias
         SOUND: (str, None)},       # generate SOUND object
        {"alias": (str, "name"),    # default value == dependent on
         "lang": (str, "default_lang")} # look first self, then settings
    ]

    def __init__(self, **kwargs):
        """ define Role object """
        print(f"\nRole __init__ ()")
        for key, value in kwargs.items():
            print(f">{key} = {value}")
        super().__init__(**kwargs)

    def do(self, **kwargs):
        """
        Do Role object call
        :param kwargs: overriding parameterss
        :return: None
        """
        print(f"\nRole do()")
        for key, value in kwargs.items():
            print(f">{key} = {value}")
        text_ = kwargs.pop(VALUES, "")
        sound_name = kwargs.get(SOUND, None)
        if text_ == "":
            text_ = self.alias
            kwargs[VALUES] = text_
            like = kwargs.get('like', NARRATOR)
            # object 'like' is taken in to account
            # ONLY IF speaking alias name == no initial text
            try:
                # First use "like"'s parameters
                me = copy.deepcopy(defined_actions[like])
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
        if sound_name in defined_actions.keys():
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


def create_sound(sound_name, **kwargs):
    object_ = DEFINING_ACTIONS[SOUND](
        name=sound_name, __VALUES__=add_quotes(sound_name), **kwargs)
    defined_actions[sound_name] = object_
    return sound_name, \
       object_, \
       {"name": , VALUES: sound_name, **kwargs}


class Sound(Definition):
    """ Define Sound object
    (SOUND name (input list of sounds and filenames  to be joined
    (gain g)  (start s) (end e)
    (cross_fade c) <-- not for the last (1 ==> error?)
    (fade_in fi) (fade_out fo)
    (overlay, position, gain_during_overlay, loop, times)
    (apply_gain, fade, from_gain , to_gain
    more: https://github.com/jiaaro/pydub/blob/master/API.markdown
    )
    """
    params = [
        {},     # new name
        {VALUES: (str, None),
         "gain": (float, 1.0),
         "input": (list_, []),    # (sound|filename)*
         "audio": (as_is, None),  # possible AudioSegment object
         "export": (str, ""),     # save sound
         "start": (int, 0),
         "end": (int, -1),
         "remove_start": (int, -1),
         "remove_end": (int, 0)},
        {}
    ]

    def __init__(self, **kwargs):
        """ Define Sound object """
        print("\nSound.__init__():")
        for key, value in kwargs.items():
            print(f">{key} = {value}")
        super().__init__(**kwargs)
        #
        # Process input == list of sound/files
        #
        print(f"Sound._iinit: {self.input}")
        sounds = [get_sound(sf) for sf in self.input]
        # Process other parameters
        #---
        # Join
        audio = sounds[0]
        for sound in sounds[1:]:
            audio += sound
        self.audio = audio

    def do(self, **kwargs):
        """
        Do Sound object call
        :param kwargs: overriding parameters
        :return: None
        """

        print("\n1 Sound.__do__():")
        for key, value in kwargs.items():
            print(f">{key} = {value}")
        if kwargs.get("input", "") == "":
            try:
                kwargs["input"] = self.name
                print(f" x Sound.do ()->sounds={kwargs['input']}")
            except Exception as e:
                print(f"Failed {e}")
                pass
        print("\n2 Sound.__do__():")
        for key, value in kwargs.items():
            print(f">>{key} = {value}")

        me = super().do(**kwargs)
        print(f">>>  Sound.do ()->sounds={me.__dict__['input']}")
        sounds_and_files = me.__dict__["input"]
        #### VALUES --> input!!!!!
        sounds = []################VVVVVVV ON STRING!
        for sound_or_file in sounds_and_files:
            sound_or_file = remove_quotes(sound_or_file)
            print(f"-1->sound_or_file={sound_or_file}")
            sound = defined_actions.get(sound_or_file, None)
            print(f"-2---->sound={sound}")
            if sound is None:
                try:
                    sound = AudioSegment.from_mp3(sound_or_file)
                    print(f"-3------->sound={sound}")
                except:
                    print(f"*** Mp3 file {sound_or_file} not found, skipped.")
                    pass
            else:
                sound = sound.audio
                print(f"-4----------------->sound={sound}")
            if sound is not None:
                sounds.append(sound)
        print(f">> sounds={sounds}")
        print(f"call add_sound {sounds[0]} {type(sounds[0])}")
        add_sound(sounds[0])
        #
        # Make new SOUND
        #if kwargs.get(SOUND, None) is not None:
        #    self.audio =
        #
        #
        # Export sound
        #
        export = kwargs.pop("export", "")
        if export != "":
            sounds[0].export(export)


class Wait(Definition):
    """ Definition of Wait object and waiting """
    params = [
        {},
        {"time": (float, 0.5)},
        {}
    ]

    def __init__(self, **kwargs):
        """ Define Wait object """
        super().__init__(**kwargs)

    def do(self, **kwargs):
        """
        Do Wait object call
        :param kwargs: overriding parameters
        :return: None
        """
        # text_ is alternative for time
        # both defined -> error
        text_ = kwargs.pop(VALUES, "")
        time = kwargs.get(VALUES, "")
        me = super().do(**kwargs)
        if text != "" and time != "":
            #  error
            raise ValueError(f"property 'time' defined twice: values='{text_}' time='{time}'")
        if text_ == "":
            add_silence(me.time)


class Group(Definition):
    """ Definition of Group object and action"""
    params = [
        {'members': (list_, None)},
        {'gain': (float, 1.0)},
        {}
    ]

    def __init__(self, **kwargs):
        """ Define Group object """
        super().__init__(**kwargs)

    def do(self, **kwargs):
        """
        Do Group object call == call at the same time all members
        :param kwargs: parameters that temporary overrides declared values
        :return: None
        """
        text_ = kwargs.pop(VALUES, "")
        me = super().do(**kwargs)
        for member in me.members:
            print(f"member {member}: {vars(defined_actions[member])}" )


class Settings(Definition):
    """ Definition of Group object and action"""
    params = [
        {"name": (str, SETTINGS)},
        {"default_lang": (str, "fi"),
         "voice_directories":
             (lambda x: list_(". voice "+x), ". voice"),
         VALUES: (str, ""),
         # mp3 export
         "export": (str, "output.mp3"),
         "format": (str, "mp3"),
         "title": (str, ""),
         "artist": (str, "Various Artists"),
         "album": (str, ""),
         "comments": (str, ""),
         "date": (str, ""),
         "genre": (str, ""),
         "cover": (str, None),
         # play results in the end
         "play_final": (bool_, True),
         # show results
         "print_text": (bool_, False),
         "print_defined_actions": (bool_, False),
         "print_manuscript": (bool_, False),
         # debug settings
         "play_while": (bool_, False),
         "print_executions": (bool_, False)},
        {}
    ]

    def __init__(self, **kwargs):
        """ Define Group object """
        global settings
        kwargs["name"] = SETTINGS
        super().__init__(**kwargs)
        settings = self
        defined_actions[NARRATOR].__dict__['lang'] = settings.__dict__['default_lang']


DEFINING_ACTIONS = {
    ROLE: Role,
    SOUND: Sound,
    GROUP: Group,
    WAIT: Wait,
    SETTINGS: Settings,
}


class ManuscriptLexer(Lexer):
    """ Lecical analyser """

    tokens = (NAME, STRING, RPAREN)
    ignore = ' \t'
    ignore_r = r'\r'  # if UTF-8 encoding
    ignore_hashcomment = r'\(\#(?s)(.*?)\#\)'      # (#...#)
    ignore_percentcomment = r'\(%(?s)(.*?)%\)'     # (%...%)
    ignore_asteriskcomment = r'\(\*(?s)(.*?)\*\)'  # (*...*)

    NAME = r'\(\s*[^\s\#%@\*"\'\(\)]+'  # start (, no ",',(,)
    RPAREN = r'\)'
    STRING = (
        r'"[^"]*"'           # double quote string
        r"|'[^']*'"          # single quote string
        r'|[^\s@"\'\(\)]+'     # no {",',(,), ,\s}
    )

    @_(r'@(?s)(.*)')
    def eof(self, t):
        """ End-of-file: @ causes eof (for debugging purposes)
        :param t: token
        :return: None
        """
        pass

    @_(r'\n+')
    def newline(self, t):
        """ handle newlines
        :param t: token
        :return: None
        """
        self.lineno += t.value.count('\n')

    def error(self, t):
        """ Notify errors
        :param t: token
        :return: error, increase index
        """
        ill_char = ascii(t.value[0])
        print(highlight(
            f"*** Lexigal error: illegal character '{ill_char}' in line {self.lineno} column {find_column(text, t)}",
            color='red'))
        print(text.splitlines()[self.lineno-1])
        print(find_column(text, t)*" ", "^ ILLEGAL CHAR")
        self.index += 1


class ManuscriptParser(Parser):
    """ Syntax parser
    manuscript ::= manuscript part | part
    part ::= command | values
    command ::= name params ')'
    params ::= params param | param | empty
    param ::= name values ')' | values
    values ::= values STRING | STRING
    STRING ::= "..." | '...' | non-terminal string
    comment ::= (*...*) | (#...#) | (%...%)
    """
    debugfile = "parser.out"
    tokens = ManuscriptLexer.tokens

    def __init__(self):
        """ initialization """
        pass

    @_('manuscript part')
    def manuscript(self, p):
        if p.part is None:
            return p.manuscript
        return p.manuscript + [p.part]

    @_('part')
    def manuscript(self, p):
        return [p.part]

    @_('command')
    def part(self, p):
        return p.command

    @_('values')
    def part(self, p):
        return NARRATOR, defined_actions[NARRATOR], {VALUES: p.values}

    @_('NAME params RPAREN')
    def command(self, p):
        name = p.NAME[1:].strip()
        params = p.params
        values = params.pop(VALUES, "")
        # Exceptionally the settings are handled as follows
        if name == SETTINGS:
            params[VALUES] = values = SETTINGS

        if name in DEFINING_ACTIONS:
            if values == "":
                raise ValueError(
                    f" *** Line {p.lineno}: Illegal use of '{name}' - no values")
            if values not in set(defined_actions.keys()):
                object_ = DEFINING_ACTIONS[name](name=values, **params)
                defined_actions[values] = object_
                return name, DEFINING_ACTIONS[name], {"name": values, **params}
            raise ValueError(
                f" *** Line {p.lineno}: Double {name} definition '{values}'")
        if name in defined_actions.keys():
            return name, defined_actions[name], {VALUES: values, **params}
        #
        # Non-defind action -> solve later
        #
        return name, None, {VALUES: values, **params}

    @_('params param')
    def params(self, p):
        if list(p.param.keys())[0] not in p.params.keys():
            return {**p.params, **p.param}
        return p.params

    @_('param')
    def params(self, p):
        return p.param

    @_('empty')
    def params(self, p):
        return {}

    @_('')
    def empty(self, p):
        pass

    @_('values')
    def params(self, p):
        return {VALUES: p.values}

    @_('NAME values RPAREN')
    def param(self, p):
        return {p.NAME[1:].strip(): p.values}

    @_('values STRING')
    def values(self, p):
        return p.values + " " + p.STRING

    @_('STRING')
    def values(self, p):
        return p.STRING

def find_column(text, token):
    """ Compute column.
    input is the input text string
    token is a token instance
    """
    last_cr = text.rfind('\n', 0, token.index)
    if last_cr < 0:
        last_cr = 0
    column = (token.index - last_cr) + 1
    return column


def lprint(header, the_list, numbers=True):
    """ List print """
    print(header)
    n = len(str(len(the_list)))
    for ielement, element in enumerate(the_list):
        if numbers:
            print(f"{ielement:{n}}   {element}")
        else:
            print(f"   {element}")


ESCAPE_CODE = "\033["
colors = {'black': 30, 'red': 31, 'green':32, 'yellow': 33, 'blue': 34, 'purple': 35, 'cyan': 36, 'white':37}
brights = {"bright "+color: value + 60 for color, value, in colors.items()}
TEXT_COLOR = {'reset': 0, **colors, **brights}
TEXT_STYLE = {'reset': 0, 'no effect': 0, 'bold': 1, 'underline': 2, 'negative1': 3, 'negative2': 5}
BACKGROUND_COLOR = {color: value+10 for color, value in TEXT_COLOR.items()}
BACKGROUND_COLOR['reset'] = 0
RESET = (ESCAPE_CODE + "0;0;0m")


def highlight(text_, color='reset', style='reset', background='reset'):
    """
    Use color and other highlights
    :param text_: text to be highlighted
    :param color: text color
    :param style: text style (reset==no effect |b old | underline | etc.)
    :param background: background color
    :return: escape-coded highlighted string, rest-code in the end
    """
    return (ESCAPE_CODE
            + str(TEXT_STYLE.get(style.lower(), 'no_effect')) + ";"
            + str(TEXT_COLOR.get(color.lower(), 'red')) + ";"
            + str(BACKGROUND_COLOR.get(background.lower(), 'black')) + "m"
            + str(text_)
            + RESET)


def back_search(searched, the_list, index=0):
    """ Search 'searched' from 'the_list' in in backwrd order """
    for ikey, key in enumerate(reversed(the_list)):
        print(f"back_search ikey={ikey} key[index]={key[index]} searched={searched}")
        if key[index] == searched:
            return ikey
    return -1


def create_playlist(the_manuscript):
    i = 0
    for command, object_, params in tqdm(the_manuscript):
        if settings.print_executions:
            print(f"\n{i} {command} {params}")
        i += 1
        if object_ is None:
            # Lazy evaluation (e.g. ROLE --> SOUND)
            print("Lazy evaluation")
            object_ = defined_actions[command]
        if isinstance(object_, Definition):
            # Object of defined action
            print("Do object")
            object_.do(**params)
        else:
            # Definition of new object
            print("Create object")
            object_(**params)


def box_print(text_lines, bc="+-+||+-+"):
    width = max([len(line) for line in text_lines])
    result = f"{bc[0]}{(width+2)*bc[1]}{bc[2]}"
    for line in text_lines:
        result +=f"\n{bc[3]} {line:^{width}} {bc[4]}"
    result += f"\n{bc[5]}{(width+2)*bc[6]}{bc[7]}"
    return result


if __name__ == "__main__":
    """ Manuscript manager
    1. create lexical analyser and parser
    2. define actors NARRATOR and BREAK
    3. parse manuscript and create list of actions
    4. make mp3 file
    5. play result file
    """
    #global playlist
    print(box_print(
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