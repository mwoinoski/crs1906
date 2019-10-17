"""
class_decorator_demo.py - example of a decorator for an entire class
From https://www.codementor.io/sheena/advanced-use-python-decorators-class-function-du107nxsv
"""

import datetime


def time_this(original_function):
    """ decorator for a single function or method """
    print("decorating")

    def new_function(*args, **kwargs):
        print("starting timer")
        before = datetime.datetime.now()
        original_result = original_function(*args, **kwargs)
        after = datetime.datetime.now()
        print(f"Elapsed Time = {after - before}")
        return original_result
    return new_function


def time_all_class_methods(cls):
    """
    class decorator that applies the time_this decorator to all methods of a class
    """
    class NewCls(object):
        def __init__(self, *args, **kwargs):
            self.obj_instance = cls(*args, **kwargs)

        def __getattribute__(self, attr_name):
            """
            this is called whenever any attribute of a NewCls object is accessed.
            This function first tries to  get the attribute off NewCls. If it
            fails then it tries to fetch the attribute from self.obj_instance (an
            instance of the decorated class). If it manages to fetch the attribute
            from self.obj_instance and the attribute is an instance method then
            `time_this` is applied.
            """
            try:
                return super().__getattribute__(attr_name)
            except AttributeError:
                attr_value = self.obj_instance.__getattribute__(attr_name)
                if isinstance(attr_value, type(self.__init__)):  # it is an instance method
                    return time_this(attr_value)                 # this is equivalent of just decorating the method with time_this
                else:
                    return attr_value
    return NewCls


import time


@time_all_class_methods
class DemoClassDecorator(object):
    def __init__(self, delay=1):
        self.delay = delay

    def method1(self):
        print("entering method1")
        time.sleep(self.delay)
        print("exiting method1")

    def method2(self):
        print("entering method2")
        time.sleep(self.delay + 1)
        print("exiting method2")


demo = DemoClassDecorator()
demo.method1()
demo.method2()
