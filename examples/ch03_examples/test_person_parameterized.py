r"""
Parameterized unit tests for Person

Run as follows:
cd C:\crs1906\examples\ch03_examples
pytest test_person_parameterized.py
"""

from pytest import mark

from person import Person


@mark.parametrize('first, middle, last, expected', [
    ("John", None, "Adams", "John Adams"),
    ("John", "Quincy", "Adams", "John Quincy Adams"),
    ("John", "", "Adams", "John Adams"),
    ("John", None, "Adams", "John Adams"),
    (None, None, "Coltrane", "Coltrane"),
    ("Miles", None, None, "Miles"), 
    (None, "Quincy", None, "Quincy"), 
])
def test_full_name(first, middle, last, expected):
    person = Person(first, middle, last)

    full_name = person.full_name()

    assert expected == full_name
