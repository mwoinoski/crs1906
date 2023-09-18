r"""
Unit tests for Person

Run as follows:
	cd C:\crs1906\examples\ch03_examples
	pytest test_person_fail.py
"""

from person_buggy import Person

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'


def test_init():
	person = Person("John", "Quincy", "Adams")

	assert "John" == person.first_name
	assert "Quincy" == person.middle_name
	assert "Adams" == person.last_name

def test_full_name():
	person = Person("John", "Quincy", "Adams")
	full_name = person.full_name()
	assert "John Quincy Adams" == full_name

def test_empty_middle():
	person = Person("John", "", "Adams")
	full_name = person.full_name()
	assert "John Adams" == full_name

def test_full_name_first_only():
	person = Person("John", None, None)
	full_name = person.full_name()
	assert "John" == full_name

def test_full_name_middle_only():
	person = Person(None, "Quincy", None)
	full_name = person.full_name()
	assert "Quincy" == full_name
