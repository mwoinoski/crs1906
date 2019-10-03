"""
mixin_class.py - Example of a mixin class
"""


class ComparableMixin(object):
    """This class has methods which use `<=` and `==`,
    but this class does NOT implement those methods."""
    def __init__(self):
        print('ComparableMixin.__init__')

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self <= other and (self != other)

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return self == other or self > other


class SimpleCounter:
    def __init__(self, start):
        print('SimpleCounter.__init__')
        self._count = start

    def increment(self, incr=1):
        self._count += incr
        return self._count

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value

    def __str__(self):
        return 'count={}'.format(self.count)

class UpAndDownCounter(SimpleCounter, ComparableMixin):
    """UpAndDownCounter uses multiple inheritance with ComparableMixin"""

    def __init__(self, start, min_value=0):
        print('UpAndDownCounter.__init__')
        super().__init__(start)
        self._min = min_value

    def decrement(self, incr=1):
        if self.count > self._min:
            self.count -= incr
        return self.count

    def __le__(self, other):
        return self._count <= other.count

    def __eq__(self, other):
        return self._count == other.count

    def __str__(self):
        return super().__str__() + ',min={}'.format(self._min)


counter0 = UpAndDownCounter(0)
counter1 = UpAndDownCounter(1)

assert counter0 == counter0
assert counter0 <= counter1
assert counter0 < counter1
assert counter0 != counter1
assert counter1 > counter0
assert counter1 >= counter1

print(counter0.increment())
print(counter0.decrement())