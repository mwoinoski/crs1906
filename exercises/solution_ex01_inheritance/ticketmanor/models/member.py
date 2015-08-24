"""
Member model class
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

# TODO: import the Person class from the person module
from ticketmanor.models.person import Person
# Note that a relative import also works:
# from .person import Person


# TODO: make Member a subclass of Person
class Member(Person):
    """
    Model class for Member
    """

    def __init__(self, first_name, last_name, email, middles=None,
                 street=None, city=None, state=None, country=None,
                 post_code=None, nick_name=None, profile_photo=None):

        # TODO: call the superclass __init__() method, passing the
        # appropriate arguments
        super().__init__(first_name, last_name, email, middles, street, city,
                         state, country, post_code)

        # TODO: save the remaining arguments in data attributes of the
        # current Member object
        self.nick_name = nick_name
        self.profile_photo = profile_photo

    # TODO: Modify the methods here to delegate as much work as possible to
    # your Person methods
    # HINT: you will be able to delete some methods completely; others can
    # override the superclass methods and then call the superclass methods to
    # do part of the work.

    def __eq__(self, other):
        """Compare Member instances."""
        return super().__eq__(other) and \
            other.nick_name == self.nick_name and \
            other.profile_photo == self.profile_photo

    def __str__(self):
        """Return a human-readable representation of a Member"""
        return super().__str__() + ' ' + self.nick_name

    def __repr__(self):
        """Return an unambiguous String representation of a Member"""
        return super().__repr_() + \
            ",nick_name={self.nick_name},profile_photo={self.profile_photo}" \
            .format(self=self)

    # def name(self):
    #     middle_name = self.middles + " " if self.middles is not None else ""
    #     return "{self.first_name} {}{self.last_name}"\
    #         .format(middle_name, self=self)
    #
    # def __eq__(self, other):
    #     """Compare Member instances."""
    #     return isinstance(other, self.__class__) and \
    #         other.first_name == self.first_name and \
    #         other.middles == self.middles and \
    #         other.last_name == self.last_name and \
    #         other.email == self.email and \
    #         other.street == self.street and \
    #         other.city == self.city and \
    #         other.state == self.state and \
    #         other.country == self.country and \
    #         other.post_code == self.post_code and \
    #         other.nick_name == self.nick_name and \
    #         other.profile_photo == self.profile_photo
    #
    # def __ne__(self, other):
    #     """Compare Member instances."""
    #     return not self.__eq__(other)
    #
    # def __str__(self):
    #     """Return a human-readable representation of a Member"""
    #     return self.name + " " + self.email
    #
    # def __repr__(self):
    #     """Return an unambiguous String representation of a Member"""
    #     return "id={self.id},first_name='{self.first_name}'," \
    #         "middles='{self.middles}',last_name='{self.last_name}'," \
    #         "email='{self.email}',street='{self.street}'," \
    #         "city='{self.city}',state='{self.state}'," \
    #         "country='{self.country}',post_code='{self.post_code}',"\
    #         ",nick_name={self.nick_name},profile_photo={self.profile_photo}" \
    #         .format(self=self)
