"""
reverse.py - Demo of Iterator design pattern from Chapter 1
"""


class Reverse:
    """Class implements iterator to iterate a sequence in reverse"""
    def __init__(self, sequence):
        self.list_data = sequence
        self.index = len(sequence)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index -= 1
        return self.list_data[self.index]

nums = list(range(5))  # [1, 2, 3, 4]
for item in nums:
    print(item, end=" ")
print()

rev = Reverse(nums)
for item in rev:
    print(item, end=" ")
print()

rev_odd_nums = Reverse(range(1, 10, 2))  # sequence of 1 through 9 stepping by 2
# list comprehensions work too
print(", ".join(str(item) for item in rev_odd_nums))

# strings are iterable sequences
print("".join(str(item) for item in Reverse('My kingdom for a horse')))


