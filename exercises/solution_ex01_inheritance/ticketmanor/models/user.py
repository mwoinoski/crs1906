"""
User model class
"""

from .person import Person


class User(Person):
    # TODO: note the definition of the __init__() method. The argument list
    #       includes all arguments that are duplicated in the Customer and Member
    #       classes' __init__() methods.
    #       (no code change required).
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
    #       methods, remove any references to Customer-specific attributes.

    def name(self):
        middle_name = self.middles + " " if self.middles is not None else ""
        return "{self.first_name} {}{self.last_name}"\
            .format(middle_name, self=self)

    def __eq__(self, other):
        """Compare User instances."""
        return isinstance(other, self.__class__) and \
            other.first_name == self.first_name and \
            other.middles == self.middles and \
            other.last_name == self.last_name and \
            other.email == self.email and \
            other.street == self.street and \
            other.city == self.city and \
            other.state == self.state and \
            other.country == self.country and \
            other.post_code == self.post_code

    def __ne__(self, other):
        """Compare User instances."""
        return not self.__eq__(other)

    def __str__(self):
        """Return a human-readable representation of a User"""
        return self.name() + " " + self.email

    def __repr__(self):
        """Return an unambiguous String representation of a User"""
        return "id={self.id},first_name='{self.first_name}'," \
               "middles='{self.middles}',last_name='{self.last_name}'," \
               "email='{self.email}',street='{self.street}'," \
               "city='{self.city}',state='{self.state}'," \
               "country='{self.country}',post_code='{self.post_code}'"\
               .format(self=self)
