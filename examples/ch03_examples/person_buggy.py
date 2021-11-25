r"""
person_buggy.py - Buggy Person class for Chapter 3 examples.
"""


class Person:
    """Buggy class for a unit test demo"""

    def __init__(self, first_name, middle_name, last_name):
        """ Initialize the Person's attributes """
        self.first_name = first_name if first_name else ""
        self.middle_name = middle_name if middle_name else ""
        self.last_name = last_name if middle_name else ""  # Oops!

    def full_name(self):
        # make sure empty fields don't cause problems
        names = [self.first_name, self.middle_name, self.last_name]
        return " ".join(n for n in names if n)

    def __str__(self):
        return self.full_name()

    def __repr__(self):
        return f'Person("{self.first_name}","{self.middle_name}","{self.last_name}")'

    # Oops! Forgot to define __eq__()
