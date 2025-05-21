r"""
Unit tests for a buggy Person implementation.

Run as follows:
	cd C:\crs1906\examples\ch03_examples
	pytest test_person_pytest_fail.py
"""

from person_buggy import Person

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'


def test_full_name():
	person = Person("John", "Quincy", "Adams")
	full_name = person.full_name()
	assert "John Quincy Adams" == full_name


def test_full_name_empty_middle():
	person = Person("John", "", "Adams")
	full_name = person.full_name()
	assert "John Adams" == full_name


def test_full_name_first_only():
	person = Person("Miles", None, None)
	full_name = person.full_name()
	assert "Miles" == full_name


def test_full_name_middle_only():
	person = Person(None, "Quincy", None)
	full_name = person.full_name()
	assert "Quincy" == full_name


def test_full_name_middle_and_last_only():
	person = Person("", "Quincy", "Adams")
	full_name = person.full_name()
	assert "Quincy Adams" == full_name
