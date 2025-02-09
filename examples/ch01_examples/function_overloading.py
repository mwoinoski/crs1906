"""
function_overloading.py - example of Python function overloading

Python 3.4+ adds limited support function overloading with the @singledispatch
decorator. Note that you must explicitly register each overloaded argument
type with the @add.register decorator; and at runtime, Python checks only the
type of the first argument to the function.

The function decorated by @singledisplatch is the one called by default if
nothing else matches.

There is a standard @overload decorator, but it is used only as a type hint;
it does not implement overloaded functions.
"""

from functools import singledispatch


@singledispatch
def add(arg1, arg2):
    raise NotImplementedError('Unsupported type')


@add.register(int)
def _(arg1, arg2):
    print("First argument is of type ", type(arg1))
    print(arg1 + arg2)


@add.register(str)
def _(arg1, arg2):
    print("First argument is of type ", type(arg1))
    print(arg1 + arg2)


@add.register(list)
def _(arg1, arg2):
    print("First argument is of type ", type(arg1))
    print(arg1 + arg2)


if __name__ == '__main__':
    add(1, 2)
    add('Python', 'Programming')
    add([1, 2, 3], [5, 6, 7])
