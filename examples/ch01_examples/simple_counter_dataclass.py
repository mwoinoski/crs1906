"""
Dataclass example
"""

from dataclasses import dataclass


@dataclass
class SimpleCounter:
    """
    Dataclass adds methods automatically, based on declared instance attributes:
        def __init__(self, value: int = 0, incr: int = 1)
        def __eq__, __ne__, etc.
        def __repr__
    """
    value: int = 0
    incr: int = 1

    def increment(self):
        """ Increment the counters value by the defined incr amount """
        self.value += self.incr
        return self.value


counter = SimpleCounter(100, 2)
print(f"counter after initialization: {counter}")
counter.increment()
print(f"counter after increment: {counter}")
counter2 = SimpleCounter(102, 2)
print(f"counter == counter2 ? {counter == counter2}")
