DEFAULT_PREFIX = "__tmp_"
DEFAULT_NUMLEN = 10
COUNTER_PREFIX = "__counter_"


class Counter:
    counters = {}

    def __init__(self, prefix=COUNTER_PREFIX):
        self.prefix = prefix
        if Counter.counters.get(self.prefix, 0) == 0:
            Counter.counters[self.prefix] = 0

    def __enter__(self):
        return Counter.counters[self.prefix]

    def __exit__(self, *args):
        Counter.counters[self.prefix] += 1



class UniqueCounter:
    counters = {}

    def __init__(self, prefix=DEFAULT_PREFIX):
        self.prefix = prefix
        if UniqueCounter.counters.get(self.prefix, None) is None:
            UniqueCounter.counters[self.prefix] = 0
        self.counter = UniqueCounter.counters[self.prefix]
        UniqueCounter.counters[self.prefix] += 1


def unique_name(prefix=DEFAULT_PREFIX, numlen=DEFAULT_NUMLEN):
    counter = UniqueCounter(prefix).counter
    return prefix + f"{counter:0{numlen}}"
