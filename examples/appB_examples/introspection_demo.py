"""
introspection_demo.py - Example of introspection from Chapter 2
"""


def print_docstrings(arg):
    """Prints method names and their docstrings"""

    method_names = [method for method in dir(arg)
                    if callable(getattr(arg, method))]

    # Split docstrings to remove any newlines, then re-join using blanks
    docstrings = ['{} {}'.format(name.ljust(20),
                                 ' '.join(getattr(arg, name).__doc__.split()))
                  for name in method_names]

    # Print docstrings from all methods
    print('\n'.join(docstrings))


class MyClass:
    def do_work(self):
        """Do work for the class."""
        pass

    def clean_up(self):
        """
        Clean up after work is complete.

        Client should call this method to indicate when it's finished.
        """
        pass

print_docstrings(MyClass)

