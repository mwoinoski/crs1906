r"""
Unit tests for a buggy Person implementation.

Run as follows:
	cd C:\crs1906\examples\ch03_examples
	pytest test_person_fail.py
"""

import unittest

from person_buggy import Person

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'


class PersonTestCase(unittest.TestCase):
    """Unit tests for Person"""

    def test_full_name(self):
        person = Person("John", "Quincy", "Adams")
        full_name = person.full_name()
        self.assertEqual("John Quincy Adams", full_name)

    def test_full_name_empty_middle(self):
        person = Person("John", "", "Adams")
        full_name = person.full_name()
        self.assertEqual("John Adams", full_name)

    def test_full_name_first_only(self):
        person = Person("Miles", None, None)
        full_name = person.full_name()
        self.assertEqual("Miles", full_name)

    def test_full_name_middle_only(self):
        person = Person(None, "Quincy", None)
        full_name = person.full_name()
        self.assertEqual("Quincy", full_name)

    def test_full_name_middle_and_last_only(self):
        person = Person("", "Quincy", "Adams")
        full_name = person.full_name()
        self.assertEqual("Quincy Adams", full_name)


if __name__ == '__main__':
    unittest.main()
