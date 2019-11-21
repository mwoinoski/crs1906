r"""Pytest unit tests for Person

   Run as follows:
   cd C:\crs1906\examples\ch03_examples
   py.test test_person_pytest_fail.py
"""

from person_buggy import Person
import pytest

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


# @pytest.mark.skip
# def test_eq_new_instances_equal_fail():
#     p1 = Person(None, None, None)
#     p2 = Person(None, None, None)

#     assert p1 != p2  # calls Person.__eq__()
