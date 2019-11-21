r"""
Unit tests for Person

Run as follows:
cd C:\crs1906\examples\ch03_examples
python -m unittest test_person.py
"""

import unittest

from person_buggy import Person

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'


class PersonTestCase(unittest.TestCase):
    """Unit tests for Person"""

    def test_init(self):
        person = Person("John", "Quincy", "Adams")

        self.assertEqual("John", person.first_name)
        self.assertEqual("Quincy", person.middle_name)
        self.assertEqual("Adams", person.last_name)

    def test_full_name(self):
        person = Person("John", "Quincy", "Adams")
        full_name = person.full_name()
        self.assertEqual("John Quincy Adams", full_name)

    def test_empty_middle(self):
        person = Person("John", "", "Adams")
        full_name = person.full_name()
        self.assertEqual("John Adams", full_name)

    def test_full_name_first_only(self):
        person = Person("John", None, None)
        full_name = person.full_name()
        self.assertEqual("John", full_name)

    def test_full_name_middle_only(self):
        person = Person(None, "Quincy", None)
        full_name = person.full_name()
        self.assertEqual("Quincy", full_name)


if __name__ == '__main__':
    unittest.main()
