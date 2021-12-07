r"""
Unit tests for Person

Run as follows:
cd C:\crs1906\examples\ch03_examples
python -m unittest test_person.py
"""

import unittest

import pytest

from person import Person

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'


class PersonTestCase(unittest.TestCase):
    """Unit tests for Person"""

    def test_init(self):
        person = Person("John", None, "Adams")

        self.assertEqual("John", person.first_name)
        self.assertEqual("", person.middle_name)
        self.assertEqual("Adams", person.last_name)

    def test_init_all_args_empty(self):
        with self.assertRaises(ValueError):
            person = Person("", "", "")

    def test_eq_instances_equal(self):
        p1 = Person("John", "Quincy", "Adams")
        p2 = Person("John", "Quincy", "Adams")
        self.assertEqual(p1, p2)  # assertEqual() calls p1.__eq__(p2)
        # OR: self.assertTrue(p1 == p2)

    def test_eq_instances_not_equal(self):
        p1 = Person("John", None, "Adams")
        p2 = Person("John", "Quincy", "Adams")
        self.assertNotEqual(p1, p2)  # assertNotEqual() calls p1.__ne__(p2)
        # OR: self.assertTrue(p1 != p2)

    def test_full_name(self):
        person = Person("John", "Quincy", "Adams")
        full_name = person.full_name()
        self.assertEqual("John Quincy Adams", full_name)

    def test_full_name_empty_middle(self):
        person = Person("John", "", "Adams")
        full_name = person.full_name()
        self.assertEqual("John Adams", full_name)

    @pytest.mark.xfail(reason="Person.full_name() isn't fully implemented")
    def test_full_name_null_middle(self):
        person = Person("John", None, "Adams")
        full_name = person.full_name()
        self.assertEqual("John Adams", full_name)

    @pytest.mark.xfail
    def test_full_name_last_only(self):
        person = Person(None, None, "Coltrane")
        full_name = person.full_name()
        self.assertEqual("Coltrane", full_name)

    @pytest.mark.xfail
    def test_full_name_first_only(self):
        person = Person("Miles", None, None)
        full_name = person.full_name()
        self.assertEqual("Miles", full_name)

    @pytest.mark.xfail
    def test_full_name_middle_only(self):
        person = Person(None, "Quincy", None)
        full_name = person.full_name()
        self.assertEqual("Quincy", full_name)


if __name__ == '__main__':
    unittest.main()
