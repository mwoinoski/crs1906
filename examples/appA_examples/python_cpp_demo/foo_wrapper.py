from ctypes import cdll
lib = cdll.LoadLibrary('./libfoo.so')

class Foo(object):
    def __init__(self):
        self.obj = lib.Foo_new()

    def bar(self):
        lib.Foo_bar(self.obj)

if __name__ == '__main__':
	f = Foo()
	f.bar() #and you will see "Hello" on the screen

# Much easier to interface with Cython
# See http://docs.cython.org/src/userguide/wrapping_CPlusPlus.html

# Swig: supports up to Py 3.0 only

# Boost.Python: supports Py 3
# See http://stackoverflow.com/questions/5539557/boost-and-python-3-x
