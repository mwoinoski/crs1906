"""
metaclass_demo.py - Example of a metaclass from Chapter 2
"""

from simple_counter import SimpleCounter


class MyMeta(type):
    def __new__(meta_cls, cls_name, base_cls, cls_attrs):
        print('\n---- in MyMeta.__new__(): cls_name: ', cls_name, '----')
        print('Metaclass: ', meta_cls)
        print('Base classes: ', base_cls)
        print('Class attributes: ', cls_attrs)
        return super().__new__(meta_cls, cls_name, base_cls, cls_attrs)

    def __init__(cls, cls_name, base_cls, cls_attrs):
        print('\n---- in MyMeta.__init__(): cls_name: ', cls_name, '----')
        print('Class: ', cls)
        print('Base classes: ', base_cls)
        print('Class attributes: ', cls_attrs)
        super().__init__(cls_name, base_cls, cls_attrs)

class MaxCounter(SimpleCounter, metaclass=MyMeta):
    max_count = 0

    def __new__(cls, *args, **kwargs):
        print('---- in MaxCounter.__new__() ----')
        return super().__new__(cls)

    def __init__(self, start, max_count=100):
        print('---- in MaxCounter.__init__(): start: ', start, '----')
        super().__init__(start)
        MaxCounter.max_count = max_count

print()
mc1 = MaxCounter(0, 1000)
mc2 = MaxCounter(40, 50)
mc3 = MaxCounter(1)
print()
print(mc1.count)
print(MaxCounter.max_count)
