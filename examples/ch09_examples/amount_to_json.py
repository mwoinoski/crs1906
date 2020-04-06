"""
amount_to_json.py - Example of using a conversion function to convert an object
to JSON
"""

import json


class Amount:
    def __init__(self, value, currency):
        self.value = value
        self.currency = currency

    def __str__(self):
        return f'value={self.currency}, currency={self.currency}'


# conversion function
def get_attr_values(obj):
    return obj.__dict__


amt_obj = Amount(65.4, 'SEK')
amt_json = json.dumps(amt_obj, default=get_attr_values)

print(f'JSON for Amount({amt_obj}): {amt_json}')

# If the conversion function is very simple, you can replace it with a lambda
amt_json_lambda = json.dumps(amt_obj, default=lambda obj: obj.__dict__)

print(f'JSON for Amount({amt_obj}) (converted with a lambda): {amt_json_lambda}')
