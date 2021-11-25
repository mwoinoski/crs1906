"""
Demo of class attributes, class methods, and static methods
from Chapter 1 Python Object-Oriented Programming
"""

class SimpleCounter:
    """A simple example class"""
    how_many_counters = 0

    def __init__(self, start):
        self.count = start
        SimpleCounter.how_many_counters += 1

    @classmethod
    def get_instance_count(cls):  # parameter is type, not instance
        return cls.how_many_counters
        # or SimpleCounter.how_many_counters

    def increment(self, incr=1):
        self.count += incr
        return self.count

    def __str__(self):
        return f'count={self.count}'

counter1 = SimpleCounter(0)
counter2 = SimpleCounter(100)

print(counter1.count)
counter1.count += 1
print(counter1.count)

counter2.increment(5)
msg = "Counter2 value: " + str(counter2)
print(msg)

print(f"There are {SimpleCounter.how_many_counters}", 
      "SimpleCounter instances (class data attribute)")
print(f"There are {SimpleCounter.get_instance_count()}",
      "SimpleCounter instances (class method)")
