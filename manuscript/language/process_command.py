import manuscript.tools.constants as mc
from manuscript.messages.messages import message_text


def process_command(name, params, values, line_number, producer):
    """
    Process command NAME params ')'

    Cases:
        (1) if name is defining action without values ==> raise Error
        (2) if name is defining actin but values is already defned action ==> raise Error
        (3) if name is defining action and values not defined return
            tuple (nmae, corresp. definnig action, params added by name==values)
        (4) if name is defined action return
            tuple (name, corresp. defined actions, params added by VALUES==values)
        (5) if name is not defiing nor defined action,
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
    producer:       object of Settings
        the object which has e.g. the settings

    Returns
    -------
        tuple (name, object, params)
    """


    # Exceptionally the 'settings' are handled as follows
    if name == mc.SETTINGS:
        values = mc.SETTINGS
        params[mc.VALUES] = mc.SETTINGS

    if name in producer.defining_actions:
        # Create new object ==> VALUES is the new name and must be given
        if values == "":
            raise ValueError(message_text("C8010", (p.lineno, name)))
        if values not in set(producer.defined_actions.keys()):
            # same objet is not allowed to be generated
            # TODO: This must be rethinked since re-creation would save memory
            #       Perhaps allowing temporary names, e.g. starung with _-character
            object_ = producer.defining_actions[name](name=values, **params)
            producer.define_action(values, object_)
            # print(f"-->Defining action!")
            return name, producer.defining_actions[name], {"name": values, **params}
        raise ValueError(message_text("C8020", (line_number, name, values)))

    if name in producer.defined_actions.keys():
        # print(f"-->Defined action")
        return name, producer.defined_actions[name], {mc.VALUES: values, **params}
    #
    # Non-defined action -> solve later
    #
    print(f"--> non-defined action {name}")
    return name, None, {mc.VALUES: values, **params}