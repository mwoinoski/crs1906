r"""
Unit tests for Person

Run as follows:
	cd C:\crs1906\examples\ch03_examples
	python -m unittest test_person_unittest.py
"""

from pytest import raises

from person import Person

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'


def test_init():
    person = Person("John", None, "Adams")

    assert "John" == person.first_name
    assert "" == person.middle_name
    assert "Adams" == person.last_name


# TODO: Add a test case that calls the Person constructor with three arguments.
#       Each argument should contain leading and trailing spaces.
# HINT: Copy the first test case and modify it as needed.


def test_full_name():
    person = Person("John", "Quincy", "Adams")
    full_name = person.full_name()
    assert "John Quincy Adams" == full_name


def test_full_name_empty_middle():
    person = Person("John", "", "Adams")
    full_name = person.full_name()
    assert "John Adams" == full_name


def test_full_name_null_middle():
    person = Person("John", None, "Adams")
    full_name = person.full_name()
    assert "John Adams" == full_name


def test_full_name_last_only():
    person = Person(None, None, "Coltrane")
    full_name = person.full_name()
    assert "Coltrane" == full_name


def test_full_name_first_only():
    person = Person("Miles", None, None)
    full_name = person.full_name()
    assert "Miles" == full_name


def test_full_name_middle_only():
    person = Person(None, "Quincy", None)
    full_name = person.full_name()
    assert "Quincy" == full_name


def test_init_all_args_empty():
    with raises(ValueError):
        person = Person("", "", "")


def test_eq_instances_equal():
    p1 = Person("John", "Quincy", "Adams")
    p2 = Person("John", "Quincy", "Adams")
    assert p1 == p2  # == calls p1.__eq__(p2)


def test_eq_instances_not_equal():
    p1 = Person("John", None, "Adams")
    p2 = Person("John", "Quincy", "Adams")
    assert p1 != p2  # != calls p1.__ne__(p2)
