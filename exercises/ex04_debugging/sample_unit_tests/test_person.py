"""Unit tests for Person

   Run as follows:
   cd C:\crs1906\examples\ch03_examples
   python -m unittest test_person.py
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

import unittest

from person import Person

class PersonTestCase(unittest.TestCase):
    """Unit tests for Person"""

    def test_init(self):
        person = Person("John", "Quincy", "Adams")

        self.assertEqual("John", person.first_name)
        self.assertEqual("Quincy", person.middle_name)
        self.assertEqual("Adams", person.last_name)

    def test_eq_instances_equal(self):
        p1 = Person("John", "Quincy", "Adams")
        p2 = Person("John", "Quincy", "Adams")
        self.assertEqual(p1, p2)

    def test_eq_instances_not_equal(self):
        p1 = Person("John", None, "Adams")
        p2 = Person("John", "Quincy", "Adams")
        self.assertEqual(p1, p2)  # calls Person.__ne__()

    def test_eq_new_instances_equal(self):
        p1 = Person(None, None, None)
        p2 = Person(None, None, None)
        self.assertEqual(p1, p2)  # calls Person.__eq__()

if __name__ == '__main__':
    unittest.main()
