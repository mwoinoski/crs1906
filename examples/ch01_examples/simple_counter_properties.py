"""
simple_counter_properties.py - Example of a class with a property
"""


class SimpleCounter:
    def __init__(self, start=0):
        print('In SimpleCounter.__init__')
        self._count_history = [start]  # replace single count with list

    @property
    def count(self):
        print('In SimpleCounter.count getter')
        return self._count_history[-1]  # return latest value in history

    @count.setter
    def count(self, value):
        print('In SimpleCounter.count setter')
        self._count_history.append(value)  # add value to history

    def increment(self, incr=1):
        new_count = self._count_history[-1] + incr
        self._count_history.append(new_count)
        return new_count

    def history(self):
        return self._count_history

    def __str__(self):
        return f'count={self.count}'


c = SimpleCounter()
c.count = 10  # A hidden call to the setter method
print(c.count)  # A hidden call to the getter method
c.increment()
print(c.count)
print(f'type(c.count) = {type(c.count)}')  # Magic: c.count appears to be an int
print(f'counter history: {c.history()}')


# class SimpleCounter:
#     def __init__(self, start=0):
#         print('In SimpleCounter.__init__')
#         self._count_history = [start]  # replace single count with list
#
#     def get_count(self):
#         print('In SimpleCounter.count getter')
#         return self._count_history[-1]  # return latest value in history
#
#     def set_count(self, value):
#         print('In SimpleCounter.count setter')
#         self._count_history.append(value)  # add value to history
#
#     # create a property object and assign it to a class attribute
#     # see https://docs.python.org/3/library/functions.html?highlight=property#property
#     count = property(fget=get_count, fset=set_count)
#
#     def increment(self, incr=1):
#         new_count = self._count_history[-1] + incr
#         self._count_history.append(new_count)
#         return new_count
#
#     def history(self):
#         return self._count_history
#
#     def __str__(self):
#         return f'count={self.count}'
#
#
# c = SimpleCounter()
# c.count = 10  # A hidden call to the setter method
# print(c.count)  # A hidden call to the getter method
# c.increment()
# print(c.count)
# print(f'type(c.count) = {type(c.count)}')  # Magic: c.count appears to be an int
# print(f'counter history: {c.history()}')
