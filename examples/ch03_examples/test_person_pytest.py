r"""
Unit tests for Person

Run as follows:
	cd C:\crs1906\examples\ch03_examples
	pytest test_person_pytest.py
"""

from pytest import raises

from person import Person

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'


def test_init():
	person = Person("John", "Quincy", "Adams")

	assert ("John", "Quincy", "Adams") == \
		   (person.first_name, person.middle_name, person.last_name)


def test_init_no_middle_name():
	person = Person("John", None, "Adams")

	assert ("John", "", "Adams") == \
		   (person.first_name, person.middle_name, person.last_name)

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
		Person("", "", "")

def test_eq_instances_equal():
	p1 = Person("John", "Quincy", "Adams")
	p2 = Person("John", "Quincy", "Adams")

	assert p1 == p2  # == calls p1.__eq__(p2)

def test_eq_instances_not_equal():
	p1 = Person("John", None, "Adams")
	p2 = Person("John", "Quincy", "Adams")

	assert p1 != p2  # != calls p1.__ne__(p2) if __ne__ is defined, otherwise calls !p1.__eq__(p2)

# @pytest.mark.skip(reason="Not yet implemented")  # you can skip tests
# def test_eq_new_instances_equal_fail():
#     p1 = Person(None, None, None)
#     p2 = Person(None, None, None)
#
#     assert p1 != p2  # calls Person.__eq__()
