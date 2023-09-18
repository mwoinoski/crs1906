r"""
Unit tests for Person

Run as follows:
	cd C:\crs1906\examples\ch03_examples
	pytest test_person_pytest_fail.py
"""

from pytest import raises

from person_buggy import Person

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'


def test_init():
	person = Person("John", "Quincy", "Adams")

	assert ("John", "Quincy", "Adams") == \
		   (person.first_name, person.middle_name, person.last_name)

def test_full_name():
	person = Person("John", "Quincy", "Adams")

	full_name = person.full_name()

	assert "John Quincy Adams" == full_name

def test_eq_instances_equal():
	p1 = Person("John", "Quincy", "Adams")
	p2 = Person("John", "Quincy", "Adams")

	assert p1 == p2  # == calls p1.__eq__(p2)

