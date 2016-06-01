"""
Address model class
"""
import json

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'


class Address:
    """Model class for Address

    There is no ADDRESS table; instead, an Address instance is populated
    from columns in the PEOPLE table. SQLAlchemy refers to this as the
    Composite pattern.

    See http://docs.sqlalchemy.org/en/latest/orm/composites.html
    """
    def __init__(self, street, city, state, country, post_code):
        self.street = street
        self.city = city
        self.state = state
        self.country = country
        self.post_code = post_code

    def __composite_values__(self):
        """__composite_values__ must return a tuple of all attributes"""
        return self.street, self.city, self.state, self.country, self.post_code

    def __eq__(self, other):
        """Composite class must define __eq__"""
        return isinstance(other, self.__class__) and \
            other.street == self.street and \
            other.city == self.city and \
            other.state == self.state and \
            other.country == self.country and \
            other.post_code == self.post_code

    def __ne__(self, other):
        """composite class must define __ne__"""
        return not self.__eq__(other)

    def __str__(self):
        """Returns a human-readable representation of a Address"""
        return "{self.street}, {self.city} {self.state} {self.country} " \
               "{self.post_code}".format(self=self)

    def __repr__(self):
        """Returns an unambiguous String representation of an Address"""
        return json.dumps(self.__json__(None))

    def __json__(self, request):
        """Returns a JSON representation of the Address.

        This method is required for Pyramid to serialize Address to JSON"""
        return {
            "street": self.street,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "post_code": self.post_code
        }

    def from_json(self, json_value):
        # BONUS TODO: replace the following loop with a dictionary comprehension
        # json_sanitized = {}
        # for k in json_copy:
        #     v = json_copy[k]
        #     if v == 'null':
        #         v = None
        #     json_sanitized[k] = v
        json_sanitized = {k: (None if v == 'null' else v)
                          for k, v in json_value.items()}
        self.__dict__.update(**json_sanitized)

