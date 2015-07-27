"""
vending_machine.py - Example of a State Machine Implementation
from Chapter 6
"""

from enum import Enum
from state_machine import StateMachine, State, Transition


class Coin(Enum):
    """Event class for vending machine"""
    nickel = 5
    dime = 10
    quarter = 25
    half_dollar = 50
    dollar = 100


class VendingMachine(StateMachine):
    """Vending machine simulated with a state machine"""
    cent = '\N{CENT SIGN}'  # Unicode US cent sign

    def start(self):
        """Start the state machine"""
        self.change = 0
        super().start()

    def set_change(self, change):
        """Set amount of change to be returned"""
        self.change = change

    def display(self, msg):
        """Update the message on the vending machine's display"""
        print(msg)

    def dispense(self, event):
        """Dispense merchandise"""
        self.display("Dispensing...")
        if self.change > 0:
            self.display("You get {} change".format(
                str(self.change) + VendingMachine.cent))
        else:
            self.display("No change due")

    def __init__(self):
        """Set up the vending state machine"""
        c = VendingMachine.cent  # Unicode US cent sign
        self.change = 0

        self.start_state = State(
            name='start',
            enter_action=lambda: self.display('\nTo dispense, enter 25' + c),
            transitions=[
                Transition(event=Coin.nickel, target=lambda: self.got_5),
                Transition(event=Coin.dime, target=lambda: self.got_10),
                Transition(event=Coin.quarter, target=lambda: self.dispensing)
                ])

        self.got_5 = State(
            name='got_5',
            enter_action=lambda event: self.display('You entered: 5' + c),
            transitions=[
                Transition(event=Coin.nickel, target=lambda: self.got_10),
                Transition(event=Coin.dime, target=lambda: self.got_15),
                Transition(event=Coin.quarter, target=lambda: self.dispensing,
                           action=lambda _: self.set_change(5))
                ])

        self.got_10 = State(
            name='got_10',
            enter_action=lambda event: self.display('You entered: 10' + c),
            transitions=[
                Transition(event=Coin.nickel, target=lambda: self.got_15),
                Transition(event=Coin.dime, target=lambda: self.got_20),
                Transition(event=Coin.quarter, target=lambda: self.dispensing,
                           action=lambda _: self.set_change(10))
                ])

        self.got_15 = State(
            name='got_15',
            enter_action=lambda event: self.display('You entered: 15' + c),
            transitions=[
                Transition(event=Coin.nickel, target=lambda: self.got_20),
                Transition(event=Coin.dime, target=lambda: self.dispensing),
                Transition(event=Coin.quarter, target=lambda: self.dispensing,
                           action=lambda _: self.set_change(15))
                ])

        self.got_20 = State(
            name='got_20',
            enter_action=lambda event: self.display('You entered: 20' + c),
            transitions=[
                Transition(event=Coin.nickel, target=lambda: self.dispensing),
                Transition(event=Coin.dime, target=lambda: self.dispensing,
                           action=lambda _: self.set_change(5)),
                Transition(event=Coin.quarter, target=lambda: self.dispensing,
                           action=lambda _: self.set_change(20))
                ])

        self.dispensing = State(
            name='dispensing',
            enter_action=lambda event: self.dispense(event),
            transitions=None)

        super().__init__(states=[
            self.start_state,
            self.got_5,
            self.got_10,
            self.got_15,
            self.got_20,
            self.dispensing
            ])
