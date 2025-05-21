r"""
person.py - Simple Person class for Chapter 3 examples.
"""


class Person:
    """Simple class for a unit test demo"""

    # TODO: modify this constructor as needed to make your new test case pass
    def __init__(self, first_name, middle_name, last_name):
        """ Initialize the Person's attributes """
        if not (first_name or middle_name or last_name):
            raise ValueError("All arguments are empty or None")
        # replace None with an empty string
        self.first_name = first_name.strip() if first_name else ""
        self.middle_name = middle_name.strip() if middle_name else ""
        self.last_name = last_name.strip() if last_name else ""

    def full_name(self):
        # make sure empty fields don't insert extra spaces
        names = [self.first_name, self.middle_name, self.last_name]
        return " ".join(n for n in names if n)

    def __eq__(self, other):
        """ Called when Person instances are compared with == operator """
        return isinstance(other, Person) and \
            other.first_name == self.first_name and \
            other.middle_name == self.middle_name and \
            other.last_name == self.last_name

    def __str__(self):
        """ Informal string representation of the object: human readable """
        return self.full_name()

    def __repr__(self):
        """
        Formal string representation: a valid Python expression that could be
        used to re-create the object; for example, a constructor call.
        """
        return f'Person("{self.first_name}","{self.middle_name}","{self.last_name}")'
