import manuscript.tools.constants as mc
from manuscript.messages.messages import message_text

from manuscript.elements.role import Role
from manuscript.elements.sound import Sound

from manuscript.tools.counter import unique_name


def process_command(name, params, values, line_number, work):
    """
    Process command NAME params ')'

    First Phase (parse textual manuscript to parsed manuscript)

    Cases:
        (1) SETTINGS can be redefined
        (2) Defining action without name --> Error
        (3) Defining action with old name allowed to be re-defined --> Error
        (4) Defining action with allowed name (the defining action knows how)
            (a) if all parameters defined -> define object, substitute parameters' default values
                * ROLE without SOUND-parameter -> define Role-object
                * ROLE with SOUND-parameter -> create audio -> define Sound-object
                * SOUND -> process sounds -> define Sound-object
                * WAIT -> define Wait(Sound?)-object
                * GROUP -> defined Group-object (list of defined Role.objects)
                * SETTINGS ->  if necessary overwrite previous settings
            (b) at least one parameter not fully defined ->
                * defining action != SOUND --> Error
                * defining action == SOUND --> define lazy object (audio=None), with parameters


    Second Phase (process parsed manuscript to audio)

    Cases:
        (1) Defining action ->- not executed
        (2) executable object --> execute object.do() and add audio
            make a copy and process the copy with parameters
            * Role-object --> substitute parameters values -> create audio -> return audio
            * Sound-object --> parameters? --> return audio
            * Wait/Sound-object --> parameters? --> return audio
            * Group-object --> create audios and overlay them to one audio -> return audio
        (3) lazy (SOUND) object --> try to define new (SOUND) object and execute it

    Parameters
    ----------
    name :          string
        name of the command (the leading '(' is already removed)
    params:         list
        list of given parameters
    values:         list
        string of VALUES i.e. value of the parameter without name
    line_number:    int
        the corresponding line number
    work:           object of Settings
        the object which has e.g. the settings

    Returns
    -------
        tuple (name, object, params)
    """
    print(f"process_command: {(name, params, values, line_number, work)}")
    # Exceptionally the 'settings' are handled as follows
    if name == mc.SETTINGS:
        print("++> name is SETTINGS")
        values = mc.SETTINGS
        params[mc.VALUES] = mc.SETTINGS

    sound_param = params.get(mc.SOUND, "")

    if name in work.defining_actions:
        print(f"++> name {name} is in defining actions")
        if sound_param != "":
            raise ValueError(f"*** SOUND parameter illegal in defining action '{name}'")
        # Create new object ==> VALUES is the new name and must be given
        if values == "":
            raise ValueError(message_text(work, "C8010", (line_number, name)))
        if work.definition_allowed(values):
            object_ = work.defining_actions[name](work, name=values, **params)
            print(f"process command: {name}-->{object_.name}:{object_}")
            return name, object_, {"name": values, **params}
        print(f"*** Illegal double definition {(line_number, name, values)}")
        raise ValueError(message_text(work, "C8020", (line_number, name, values)))


    if name in work.defined_actions.keys():
        print(f"++> name {name} is a defined actions")
        if work.definition_allowed(sound_param):
            # create (and define) lazy SOUND object (gets its value later)
            sound_object = Sound(work, name=sound_param)
            print(f"created lazy sound_object {sound_object}")
        # add object
        object_ = work.defined_actions[name]
        print(f"object:={object_} type={type(object_)}")
        print(f"isinstance(object_, Sound)={isinstance(object_, Sound)} values={values}")
        if not isinstance(object_, Sound) or values == "":
            pars = {mc.VALUES: values, **params}
            print(f"return {name}, object:={object_} type={type(object_)}, {pars}")
            return name, object_, {mc.VALUES: values, **params}

    print("++> name is NEW --> treat as SOUND object")
    # TODO: e.g. (meow.mp3) or (vuh miau vuh vuh) <-- vuh is defined or (meow.mp3 hau hau)
    # or even (list of sound-objects or filenames [params])
    # == (SOUND _tmp (input list of...) [params]) (_tmp) <_tmp cannot be used later>
    # unless (A B C (SOUND ABC) [params]) == (SOUND ABC (input A B C) [params])
    # Left: if A is Sound-object or filename or (execution of Role-/Wait-/Group-object
    # Right: A, B, and C must be Sound-objects or filenames
    # params[mc.VALUES] = name + " " + values
    params["input"] = params.get("input", "") + " " + name + " " + values
    tmp = sound_param if sound_param != "" else unique_name("#tmp_")
    object_ = Sound(work, name=tmp, **params)
    print(f"created Sound-object 2nd way tmp={tmp}")
    return tmp, object_, {}
