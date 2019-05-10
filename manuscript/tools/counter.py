class Counter:
    counters = {}

    def __init__(self, prefix='tmp'):
        self.prefix = prefix
        if Counter.counters.get(self.prefix, 0) == 0:
            Counter.counters[self.prefix] = 0

    def __enter__(self):
        return Counter.counters[self.prefix]

    def __exit__(self, *args):
        Counter.counters[self.prefix] += 1
