"""
double_list.py - Example of custom indexing from Chapter 2
"""

class DoubleList:
    def __init__(self, items):
        self.items = items

    def __getitem__(self, index):
        return self.items[index] * 2

double_list = DoubleList([100, 200, 300])
print(double_list[0])    # prints 200
