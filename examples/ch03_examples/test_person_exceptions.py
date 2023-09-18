r"""
Pytest unit tests for Person

Run as follows:
   cd C:\crs1906\examples\ch03_examples
   pytest test_person_exceptions.py
"""

from pytest import raises

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'


class Person:
    def __init__(self, name, age=None):
        if age is not None and (not isinstance(age, (int, float)) or age <= 0):
            raise ValueError(f"Invalid age {age}: age must be greater than 0")
        self.name = name
        self._age = age

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(f"Invalid age {value}: age must be greater than 0")
        self._age = value


def test_init_bad_age():
    with raises(ValueError):
        Person("Atticus Finch", 0)


def test_set_bad_age():
    person = Person("Atticus Finch")

    with raises(ValueError, match=r"[Gg]reater than (0|zero)"):
        person.age = 0
