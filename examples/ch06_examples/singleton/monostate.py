"""
monostate.py - Defines a Monostate implementation of the
Singleton design pattern
"""

from collections import OrderedDict

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'


class Monostate:
    """
    Monostate implementation of Singleton design pattern
    """
    
    _shared_state = {}  # class variable

    def __new__(cls, *args, **kwargs):
        """Called when a new instance is created"""
        obj = super().__new__(cls)  # Python 2: super(object, self)
        obj.__dict__ = cls._shared_state
        return obj


class FileCache(Monostate):
    def __init__(self):
        if not hasattr(self, "files"):
            self.files = OrderedDict()  # adds instance variable named files

    def add_file(self, filename, contents):
        self.files[filename] = contents  # add file contents to shared state

    def __str__(self):
        return "\n".join(": ".join(item) for item in self.files.items())
        # 1. for item in self.files.items(): a generator expression that
        #    yields tuples of (key, value).
        # 2. ": ".join(item): elements in the two-element tuple are joined
        #    in a string, and all the strings are yielded by a second generator
        #    expression.
        # 3. "\n".join(...): finally, all strings yielded by the second
        #    generator expression are joined with newlines.

def main():
    file_cache1 = FileCache()
    with open("file1") as f1:
        file_cache1.add_file("file1", f1.read())

    print("==== file_cache1 ====")
    print(file_cache1)

    file_cache2 = FileCache()
    with open("file2") as f2:
        file_cache2.add_file("file2", f2.read())

    print("\n==== file_cache1 ====")
    print(file_cache1)

    print("\n==== file_cache2 ====")
    print(file_cache2)

if __name__ == "__main__":
    main()