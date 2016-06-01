"""
simple_counter.py - SimpleCounter class with two subclasses
"""

class SimpleCounter:
    def __init__(self, start):
        self.count = start

    def increment(self, incr=1):
        self.count += incr
        return self.count

class UpAndDownCounter(SimpleCounter):
    def __init__(self, start, min=0):
        super().__init__(start)
        self.min = min

    def decrement(self, incr=1):
        if self.count > self.min:
            self.count -= incr
        return self.count

class BoundedCounter(SimpleCounter):
    def __init__(self, start, limit=None):
        super().__init__(start)
        self.limit = limit

    def increment(self, incr=1):
        """Overrides increment() from superclass"""
        if self.limit is not None and self.count < self.limit:
            self.count += incr
        return self.count

up_and_down = UpAndDownCounter(10)
up_and_down.increment()
up_and_down.decrement()
up_and_down.decrement()
print("up_and_down.count = " + str(up_and_down.count))

bounded = BoundedCounter(0, 2)
bounded.increment()
bounded.increment()
bounded.increment()
print("bounded.count = " + str(bounded.count))
