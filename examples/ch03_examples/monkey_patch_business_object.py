"""
monkey_patch_business_object.py - Example of monkey patching, from Chapter 3
"""
import types

from business_object import BusinessObject, UserDao

from person import Person


# Here's our monkey patch
def patch_get_user(obj, user_id):
    print("patch_get_user({}, {})".format(obj, user_id))
    return Person('Curious', '', 'George')

bus_obj = BusinessObject('Business As Usual')

person = bus_obj.get_user(123)
print('\nBefore monkey patch, person = {}'.format(person))

# Save a reference to the old method
old_get_user = BusinessObject.get_user
# Replace the class's get_user method with our monkey patch.
# Now all instances of BusinessObject have the new method.
BusinessObject.get_user = patch_get_user

person = bus_obj.get_user(123)
print('After monkey patch, person = {}'.format(person))

# Restore the old method definition
BusinessObject.get_user = old_get_user

person = bus_obj.get_user(123)
print('After replacing old method, person = {}\n'.format(person))

dao1 = UserDao()
dao2 = UserDao()
print('Before monkey patch, dao1.query_user = {}'.format(dao1.query_user(123)))
print('Before monkey patch, dao2.query_user = {}'.format(dao2.query_user(123)))

# This time, we patch only one instance, not the entire class.
# This requires a call to types.MethodType to bind the new function to
# the instance. This ensures that dao2 will be passed as 'self'.
dao2.query_user = types.MethodType(patch_get_user, dao2)

# dao1 has the old method, dao2 has the new method
print('After monkey patch, dao1.query_user = {}'.format(dao1.query_user(123)))
print('After monkey patch, dao2.query_user = {}'.format(dao2.query_user(123)))
