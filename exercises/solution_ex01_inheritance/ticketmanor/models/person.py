"""
Person model class
"""


class Person:
    """
    Model class for Person
    """

    # TODO: define an __init__() method. The argument list to __init__() should
    # include all the arguments that are duplicated in the Customer and Member
    # classes' __init__() methods.
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

    def name(self):
        middle_name = self.middles + " " if self.middles is not None else ""
        return "{self.first_name} {}{self.last_name}"\
            .format(middle_name, self=self)

    def __eq__(self, other):
        """Compare Person instances."""
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
        """Compare Person instances."""
        return not self.__eq__(other)

    def __str__(self):
        """Return a human-readable representation of a Person"""
        return self.name() + " " + self.email

    def __repr__(self):
        """Return an unambiguous String representation of a Person"""
        return "id={self.id},first_name='{self.first_name}'," \
               "middles='{self.middles}',last_name='{self.last_name}'," \
               "email='{self.email}',street='{self.street}'," \
               "city='{self.city}',state='{self.state}'," \
               "country='{self.country}',post_code='{self.post_code}'"\
               .format(self=self)
