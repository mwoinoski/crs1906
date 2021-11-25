# data_class_demo.py
#
# @dataclass decorator adds methods to a class: __init__(), __eq__(), __repr__()

from dataclasses import dataclass

@dataclass
class InventoryItem:
    """Class for keeping track of an item in inventory."""
    name: str
    unit_price: float
    quantity_on_hand: int = 0
    
    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand

# @dataclass adds methods automatically:
#     def __init__(self, name: str, unit_price: float, quantity_on_hand: int=0):
#         self.name = name
#         self.unit_price = unit_price
#         self.quantity_on_hand = quantity_on_hand
# 
#     def __eq__(self, other) -> bool: 
#         # true if `other` has same attributes and values as `self`
# 
#     def __repr__(self) -> str:
#         # returns string representation of `self`
#
# You can pass arguments to @dataclass to control which methods are generated.
# See the Python Standard Library > Python Runtime Services > dataclasses

# call the auto-generated constructor
item = InventoryItem('eBike', 999.99, 5)

# call the auto-generated __repr__() method
print(f'Item {item.__repr__()} total cost is {item.total_cost()}')

# string interpolation calls __repr__() method if __str__() isn't defined
print(f'Item {item} total cost is {item.total_cost()}')

# create another InventoryItem with the same attribute and values
item2 = InventoryItem('eBike', 999.99, 5)

# now check whether the objects are equal. The "==" operator calls __eq__()
print(f'The items are{"" if item == item2 else " not"} equal')
item2.quantity_on_hand -= 1
print(f'The items are now{"" if item == item2 else " not"} equal')
