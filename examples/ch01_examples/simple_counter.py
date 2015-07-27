"""
Inheritance example from Chapter 1 Python Object-Oriented Programming
"""

class SimpleCounter:
    """A simple example class"""

    def __init__(self, start):
        print("SimpleCounter.__init__(): enter")
        self.count = start
        print("SimpleCounter.__init__(): exit")

    def increment(self, incr=1):
        self.count += incr
        return self.count

    def __str__(self):
        return 'count={}'.format(self.count)

class UpAndDownCounter(SimpleCounter):
    """UpAndDownCounter defines a decrement operation"""

    def __init__(self, start, min=0):
        print("UpAndDownCounter.__init__(): enter")
        super().__init__(start)
        self.min = min
        print("UpAndDownCounter.__init__(): exit")

    # inherits increment() from base class

    def decrement(self, incr=1):
        if self.count > self.min:
            self.count -= incr
        return self.count

    def __str__(self):
        return super().__str__() + ',min={}'.format(self.min)

up_and_down = UpAndDownCounter(10)
up_and_down.increment()
up_and_down.decrement()
up_and_down.decrement()
print("up_and_down = " + str(up_and_down))
