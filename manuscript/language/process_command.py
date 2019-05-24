import manuscript.tools.constants as mc
from manuscript.messages.messages import message_text


def process_command(name, params, values, line_number, work):
    """
    Process command NAME params ')'

    First Phase (parse textual manuscript to parsed manuscript)

    Cases:
        (1) SETTINGS can be redefined
        (2) Defining action without name --> Error
        (3) Defining action with old name allowed to be re-defined --> Error
        (4) Defining action with allowed name (the definng action knows how)
            (a) if all parameters defined -> define object, substitute parameters' default values
                * ROLE without SOUND-parameter -> define Role-object
                * ROLE with SOUND-parameter -> create audio -> define Sound-object
                * SOUND -> process sounds -> define Sound-object
                * WAIT -> define Wait(Sound?)-object
                * Group -> defined Group-object (list of defined Role.objects)
                * Settings ->  if necessary overwrite previous settings
            (b) at least one parameter not fully defined ->
                * defining action != SOUND --> Error
                * defining action == SOUND --> define lazy object (auidio=None), with parameters


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

    -----------------------------------------------------------


        (1) if name is defining action without values ==> raise Error
        (2) if name is defining actin but values is already defned action ==> raise Error
        (3) if name is defining action and values not defined return
            tuple (name, corresp. definnig action, params added by name==values)
        (4) if name is defined action return
            tuple (name, corresp. defined actions, params added by VALUES==values)
        (5) if name is not defining nor defined action,
            the case must be solved later (lazy evaluation), return
            tuple (name, None as the action, params added by VALUES==values)

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
    # Exceptionally the 'settings' are handled as follows
    if name == mc.SETTINGS:
        values = mc.SETTINGS
        params[mc.VALUES] = mc.SETTINGS

    if name in work.defining_actions:
        # Create new object ==> VALUES is the new name and must be given
        if values == "":
            raise ValueError(message_text(work, "C8010", (p.lineno, name)))
        if work.definition_allowed(values):
            object_ = work.defining_actions[name](work, name=values, **params)
            #work.define_action(values, object_)
            # print(f"-->Defining action!")
            return name, object_, {"name": values, **params}
        print(f"*** Illegal double definition {(line_number, name, values)}")
        raise ValueError(message_text(work, "C8020", (line_number, name, values)))

    if name in work.defined_actions.keys():
        # print(f"-->Defined action")
        return name, work.defined_actions[name], {mc.VALUES: values, **params}
    #
    # Non-defined action -> solve later
    #
    print(f"--> non-defined action {name}")
    return name, None, {mc.VALUES: values, **params}
