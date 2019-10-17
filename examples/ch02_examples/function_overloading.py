"""
function_overloading.py - example of Python function overloading

Python 3.4+ adds limited support function overloading with the @singledispatch
decorator. Note that you must explicitly register each overloaded argument
type with the @add.register decorator; and at runtime, Python checks only the
type of the first argument to the function.

There is a standard @overload decorator, but it is used only by as a type
hint; it does not implement overloaded functions.
"""

from functools import singledispatch


@singledispatch
def add(a, b):
    raise NotImplementedError('Unsupported type')


@add.register(int)
def _(a, b):
    print("First argument is of type ", type(a))
    print(a + b)


@add.register(str)
def _(a, b):
    print("First argument is of type ", type(a))
    print(a + b)


@add.register(list)
def _(a, b):
    print("First argument is of type ", type(a))
    print(a + b)


if __name__ == '__main__':
    add(1, 2)
    add('Python', 'Programming')
    add([1, 2, 3], [5, 6, 7])
