"""Nose unit tests for Person

   Run as follows:
   pip install nose
   cd C:\crs1906\examples\ch03_examples
   nosetests test_person_nose.py
"""

from person import Person
from unittest.case import skip

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'


def test_init():
    person = Person("John", "Quincy", "Adams")

    assert ("John", "Quincy", "Adams") == \
           (person.first_name, person.middle_name, person.last_name)


def test_eq_instances_equal():
    p1 = Person("John", "Quincy", "Adams")
    p2 = Person("John", "Quincy", "Adams")

    assert p1 == p2  # calls Person.__eq__()


def test_eq_instances_not_equal():
    p1 = Person("John", None, "Adams")
    p2 = Person("John", "Quincy", "Adams")

    assert p1 != p2  # calls Person.__ne__()


def test_eq_new_instances_equal():
    p1 = Person(None, None, None)
    p2 = Person(None, None, None)

    assert p1 == p2  # calls Person.__eq__()


@skip
def test_eq_new_instances_equal_fail():
    p1 = Person(None, None, None)
    p2 = Person(None, None, None)

    assert p1 != p2  # calls Person.__eq__()
