from manuscript.elements.definition import Definition


class Action(Definition):
    params = [{"default_action": (str, None)},    # Required (== not overriddable)
              {},                                 # Optional
              {}]                                 # Dependent

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def do(self, **kwargs):
        super().do(**kwargs)