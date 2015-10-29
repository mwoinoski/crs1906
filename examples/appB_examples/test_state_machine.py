"""
test_state_machine.py - Unit tests for StateMachine
"""

import unittest

from vending_machine import VendingMachine, Coin


class TestStateMachine(unittest.TestCase):
    def test_quarter(self):
        fsm = VendingMachine()
        events = [Coin.quarter]
        fsm.start()
        for event in events:
            fsm.handle_event(event)
        self.assertEqual([fsm.start_state, fsm.dispensing], fsm.history)
        self.assertEqual(fsm.change, 0)

    def test_nickel_and_quarter(self):
        fsm = VendingMachine()
        events = [Coin.nickel, Coin.quarter]
        fsm.start()
        for event in events:
            fsm.handle_event(event)
        self.assertEqual([fsm.start_state, fsm.got_5, fsm.dispensing],
                         fsm.history)
        self.assertEqual(fsm.change, 5)

    def test_dime_and_quarter(self):
        fsm = VendingMachine()
        events = [Coin.dime, Coin.quarter]
        fsm.start()
        for event in events:
            fsm.handle_event(event)
        self.assertEqual([fsm.start_state, fsm.got_10, fsm.dispensing],
                         fsm.history)
        self.assertEqual(fsm.change, 10)

    def test_four_nickels_and_quarter(self):
        fsm = VendingMachine()
        events = [Coin.nickel, Coin.nickel, Coin.nickel, Coin.nickel,
                  Coin.quarter]
        fsm.start()
        for event in events:
            fsm.handle_event(event)
        self.assertEqual([fsm.start_state, fsm.got_5, fsm.got_10, fsm.got_15,
                          fsm.got_20, fsm.dispensing],
                         fsm.history)
        self.assertEqual(fsm.change, 20)

    def test_three_dimes(self):
        fsm = VendingMachine()
        events = [Coin.dime, Coin.dime, Coin.dime]
        fsm.start()
        for event in events:
            fsm.handle_event(event)
        self.assertEqual([fsm.start_state, fsm.got_10, fsm.got_20,
                          fsm.dispensing], fsm.history)
        self.assertEqual(fsm.change, 5)

    def test_five_nickels(self):
        fsm = VendingMachine()
        events = [Coin.nickel, Coin.nickel, Coin.nickel, Coin.nickel,
                  Coin.nickel, Coin.nickel]
        fsm.start()
        for event in events:
            fsm.handle_event(event)
        self.assertEqual([fsm.start_state, fsm.got_5, fsm.got_10, fsm.got_15,
                          fsm.got_20, fsm.dispensing], fsm.history)
        self.assertEqual(fsm.change, 0)

    def test_six_nickels(self):
        fsm = VendingMachine()
        events = [Coin.nickel, Coin.nickel, Coin.nickel, Coin.nickel,
                  Coin.nickel, Coin.nickel, Coin.nickel]
        fsm.start()
        for event in events:
            fsm.handle_event(event)
        self.assertEqual([fsm.start_state, fsm.got_5, fsm.got_10, fsm.got_15,
                          fsm.got_20, fsm.dispensing], fsm.history)
        self.assertEqual(fsm.change, 0)

    def test_half_dollar_and_quarter(self):
        fsm = VendingMachine()
        events = [Coin.half_dollar, Coin.quarter]
        fsm.start()
        for event in events:
            fsm.handle_event(event)
        self.assertEqual([fsm.start_state, fsm.dispensing], fsm.history)
        self.assertEqual(fsm.change, 0)

if __name__ == '__main__':
    unittest.main()
