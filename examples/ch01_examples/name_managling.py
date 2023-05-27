# Example of how Python applies name mangling to instance variables with names
# starting with "__". This prevents accidental modifications of data intended
# to be private, but doesn't prevent intentional modification.

class BankAccount:
    next_account_number = 1   # static/shared class level

    def __init__(self, customer, initial_deposit=0):
        # We want the account number to be "private".
        # __account_number will be mangled to _BankAccount__account_number
        self.__account_number = BankAccount.next_account_number
        BankAccount.next_account_number += 1
        self.customer = customer

        # __balance will be mangled to _BankAccount__balance
        self.__balance = initial_deposit   # balance is "private"

    def deposit(self, amount):
        self.__balance += amount

    def __str__(self):
        return f'{self.__account_number:4}  {self.customer:14} ${self.__balance:8.2f}'


a1 = BankAccount("Wilma", 300.00)
print(f'a1 = {a1}')
print(f'vars(a1) = {vars(a1)}')

# Name managling prevents accidental changes, so this adds an instance variable "__balance"
# instead of modifying the BankAccount's balance
a1.__balance = 10000

# But you can still modify the BankAccount's state using the mangled name
a1._BankAccount__balance = 10000
print(f'a1 = {a1}')
print(f'vars(a1) = {vars(a1)}')
