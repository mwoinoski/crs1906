"""
User model class
"""

from .person import Person


class User(Person):
    # TODO: note the definition of the __init__() method. The argument list
    # includes all arguments that are duplicated in the Customer and Member
    # classes' __init__() methods.
    # (no code change required).
    def __init__(self, first_name, last_name, email, middles=None,
                 street=None, city=None, state=None, country=None,
                 post_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.middles = middles
        self.street = street
        self.city = city
        self.state = state
        self.country = country
        self.post_code = post_code

    # TODO: paste methods from Customer class here. After pasting the
    # methods, remove any references to Customer-specific attributes.
