import manuscript.language.constants as mc
from manuscript.elements.definition import Definition


def process_command(name, params, values, line_number):
    """
    Process comman NAME params ')'
    :param name: name of the command (leading '(' already remved
    :param params: lists paramaters
    :param values: string of values
    :param line_number: the corresponding line number
    :return:
        (1) if name is defining action without values ==> raise Error
        (2) if name is defining actin but values is already defned action ==> raise Error
        (3) if name is defining action and values not defined return
            tuple (nmae, corresp. definnig action, params added by name==values)
        (4) if name is defined action return
            tuple (name, corresp. defined actions, params added by VALUES==values)
        (5) if name is not defiing nor defined action,
            the case must be solved later (lazy evaluation), return
            tuple (name, None as the action, params added by VALUES==values)
    """
    # Exceptionally the 'settings' are handled as follows

    print(f"process_command:\n  name={name}\n  params={params}\n  values={values}\n line_number={line_number}")
    if name == mc.SETTINGS:
        values = mc.SETTINGS
        params[mc.VALUES] = mc.SETTINGS

    if name in Definition.defining_actions:
        # Create new object ==> VALUES is the new name and must be given
        if values == "":
            raise ValueError(
                f" *** Line {p.lineno}: Illegal use of '{name}' - no values")
        if values not in set(Definition.defined_actions.keys()):
            # same objet is not allowed to be generated
            ### This must be rethinked since re-creatn woud save memory
            ### Perhaps allowing temprary names, e.g. starung with _-character
            object_ = Definition.defining_actions[name](name=values, **params)
            Definition.defined_actions[values] = object_
            #return name, {"name": values, **params}
            print(f"-->Defining action!")
            return name, Definition.defining_actions[name], {"name": values, **params}
        raise ValueError(
            f" *** Line {line_number}: Double {name} definition '{values}'")
    if name in Definition.defined_actions.keys():
        print(f"-->Defined action")
        #return name, {mc.VALUES: values, **params}
        return name, Definition.defined_actions[name], {mc.VALUES: values, **params}
    #
    # Non-defined action -> solve later
    #
    #

    print(f"--> non-defined action {name}")
    #return name, {mc.VALUES: values, **params}
    return name, None, {mc.VALUES: values, **params}