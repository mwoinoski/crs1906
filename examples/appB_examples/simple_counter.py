"""
simple_counter.py - SimpleCounter example from Chapter 2
"""

class SimpleCounter:
    """A simple example class"""

    def __init__(self, start):
        self.count = start

    def increment(self, incr=1):
        self.count += incr
        return self.count

    def __str__(self):
        return 'count={}'.format(self.count)



