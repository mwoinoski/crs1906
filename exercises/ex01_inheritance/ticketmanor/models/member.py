"""
Member model class
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

# TODO: import the User class from the ticketmanor.models.user module


# TODO: make Member a subclass of User
class Member():
    """
    Model class for Member
    """

    def __init__(self, first_name, last_name, email, middles=None,
                 street=None, city=None, state=None, country=None,
                 post_code=None, nick_name=None, profile_photo=None):

        # TODO: call the superclass __init__() method, passing the
        #       appropriate arguments


        # TODO: save any remaining arguments in data attributes of the
        #       current Customer object


        # TODO: for any argument that you passed to the superclass constructor,
        #       delete its attribute assignment from the next block of statements.
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.middles = middles
        self.street = street
        self.city = city
        self.state = state
        self.country = country
        self.post_code = post_code
        self.nick_name = nick_name
        self.profile_photo = profile_photo

    # TODO: Modify the methods here to reference Member-specific attributes
    #       when necessary, while delegating as much work as possible to superclass
    #       methods.
    # HINT: you will be able to delete some methods completely; others can
    # override the superclass methods and then call the superclass methods to
    # do part of the work.
    # HINT: add references to self.nick_name and self.profile_photo to __eq__()
    # and __repr__()

    def name(self):
        middle_name = self.middles + " " if self.middles is not None else ""
        return f"{self.first_name} {middle_name}{self.last_name}"

    def __eq__(self, other):
        """Compare Member instances."""
        return isinstance(other, self.__class__) and \
            other.first_name == self.first_name and \
            other.middles == self.middles and \
            other.last_name == self.last_name and \
            other.email == self.email and \
            other.street == self.street and \
            other.city == self.city and \
            other.state == self.state and \
            other.country == self.country and \
            other.post_code == self.post_code and \
            other.nick_name == self.nick_name and \
            other.profile_photo == self.profile_photo

    def __ne__(self, other):
        """Compare Member instances."""
        return not self.__eq__(other)

    def __str__(self):
        """Return a human-readable representation of a Member"""
        return self.name + " " + self.email

    def __repr__(self):
        """Return an unambiguous String representation of a Member"""
        return f"id={self.id},first_name='{self.first_name}'," \
            f"middles='{self.middles}',last_name='{self.last_name}'," \
            f"email='{self.email}',street='{self.street}'," \
            f"city='{self.city}',state='{self.state}'," \
            f"country='{self.country}',post_code='{self.post_code}'," \
            f",nick_name={self.nick_name},profile_photo={self.profile_photo}"
