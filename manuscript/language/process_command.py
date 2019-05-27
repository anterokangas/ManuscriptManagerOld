from manuscript.messages.messages import message_text

from manuscript.elements.sound import Sound
from manuscript.elements.work import Wait

from manuscript.tools.counter import unique_name
import manuscript.tools.constants as mc
from manuscript.tools.subclasses import get_all_subclasses


def process_command(name, params, values, line_number, work):
    """
    Process command NAME params ')'

    First Phase (parse textual manuscript to parsed manuscript)

    Error cases.
        (1) name is defining action and (params has SOUND-parameter or values is empty or values is not allowed)
    Cases:
        (1) name is defining action and values is allowed
            -> create and define object
        (2) name is instance of Sound or its subclass nad has values or parameters or nme is not defined
            -> create Sound-object(name=SOUND-param if name is SOUND, tmp otherwise
        (3) otherwise do the object

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
    if work.settings.print_executions:
        print(f"process_command {(name, params, values, line_number, work)}")

    sound_param = params.get(mc.SOUND, "")

    if name in work.defining_actions:
        if sound_param != "":
            raise ValueError(f"*** SOUND parameter illegal in defining action '{name}'")
        if values == "":
            raise ValueError(message_text(work, "C8010", (line_number, name)))

        # Create new object ==> VALUES is the new name and must be given
        if not work.definition_allowed(values):
            print(f"*** Illegal double definition {(line_number, name, values)}")
            raise ValueError(message_text(work, "C8020", (line_number, name, values)))

        object_ = work.defining_actions[name](work, name=values, **params)
        return name, object_, {"name": values, **params}

    object_ = work.defined_actions.get(name, None)
    # Case 'pure Sound-object need not to be re-created (optimized)
    additional_object_test = (
            (isinstance(object_, get_all_subclasses(Sound, True))
                and (values != "" or params != dict()))
             or object_ is None)
    if additional_object_test:
        # Create additional object
        params["input"] = " " + name + " " + values + params.get("input", "")
        params[mc.SOUND] = sound_param  # do not generate copies
        tmp = sound_param if sound_param != "" else unique_name("#tmp_")
        params["name"] = tmp
        if isinstance(object_, Wait):
            object_ = Wait(work, **params)
        else:
            object_ = Sound(work, **params)
        return tmp, object_, {}
    params[mc.VALUES] = values
    return name, object_, params
