from manuscript.elements.definition import Definition


class Action(Definition):
    params = [{},    # Required (== cannot overridden)
              {},    # Optional
              {}]    # Dependent

    def __init__(self, *args, **kwargs):
        self.params = [{**dp, **sp} for dp, sp in zip(Action.params, self.params)]
        super().__init__(*args, **kwargs)

    def do(self, *args, **kwargs):
        super().do(*args, **kwargs)
