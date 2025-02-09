"""
Customer model class
"""

__author__ = 'Mike Woinoski mike@articulatedesign.us.com'

# TODO: import the User class from the ticketmanor.models.user module
from ticketmanor.models.user import User
# Note that a relative import also works:
# from .user import User


# TODO: make Customer a subclass of User
class Customer(User):
    """
    Model class for Customer
    """

    def __init__(self, first_name, last_name, email, middles=None,
                 street=None, city=None, state=None, country=None,
                 post_code=None, customer_id=None):

        # TODO: call the superclass __init__() method, passing the
        #       appropriate arguments
        super().__init__(first_name, last_name, email, middles, street, city,
                         state, country, post_code)

        # TODO: for any argument that you passed to the superclass constructor,
        #       delete its attribute assignment from the next block of statements.
        #       Save any remaining arguments in data attributes of the current
        #       Customer object.
        self.customer_id = customer_id

    # TODO: copy all the methods below this comment and paste them into the
    #       User class

    # TODO: Modify the methods here to reference Customer-specific attributes
    #       when necessary, while delegating as much work as possible to superclass
    #       methods.

    def __eq__(self, other):
        """Compare Customer instances."""
        return super().__eq__(other) and \
            other.customer_id == self.customer_id

    def __str__(self):
        """Return a human-readable representation of a Customer"""
        return super().__str__() + ' ' + self.customer_id

    def __repr__(self):
        """Return an unambiguous String representation of a Customer"""
        return super().__repr__() + f",customer_id={self.customer_id}"

    # def name(self):
    #     middle_name = self.middles + " " if self.middles is not None else ""
    #     return f"{self.first_name} {middle_name}{self.last_name}"
    #
    # def __eq__(self, other):
    #     """Compare Customer instances."""
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
    #         other.customer_id == self.customer_id
    #
    # def __ne__(self, other):
    #     """Compare Customer instances."""
    #     return not self.__eq__(other)
    #
    # def __str__(self):
    #     """Return a human-readable representation of a Customer"""
    #     return self.name + " " + self.email
    #
    # def __repr__(self):
    #     """Return an unambiguous String representation of a Customer"""
    #     return f"id={self.id},first_name='{self.first_name}'," \
    #         f"middles='{self.middles}',last_name='{self.last_name}'," \
    #         f"email='{self.email}',street='{self.street}'," \
    #         f"city='{self.city}',state='{self.state}'," \
    #         f"country='{self.country}',post_code='{self.post_code}'," \
    #         f"customer_id='{self.customer_id}'"
