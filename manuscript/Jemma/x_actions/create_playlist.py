from tqdm import tqdm
from manuscript.actions.definition import Definition


def create_playlist(the_manuscript):
    """
    (ROLE A) --> new object Role.A
    (A text) --> A.do(text) == speak
    (A)      --> A.do(A.alias) == speak
    (A text (SOUND B)) new object Sound.B (audio=(A text))
    (A (SOUND B)) new object Sound.B (audio=(A A.alias9
    :param the_manuscript:
    :return:
    """
    i = 0
    for command, object_, params in tqdm(the_manuscript):
        if Definition.settings.print_executions:
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
