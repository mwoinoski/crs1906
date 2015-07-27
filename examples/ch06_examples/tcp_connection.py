"""
tcp_connection.py - Example of a State Machine Implementation
from Chapter 6
"""

from enum import Enum
from state_machine import StateMachine, State, Transition


class Event(Enum):
    """Event class for TCP Connection class"""
    open, acknowledge, close = range(3)


class TCPConnection(StateMachine):
    """TCP Connection simulated with a state machine"""

    def __init__(self):
        """Set up the states"""

        self.tcp_established = State(
            name='TCPEstablished',
            enter_action=lambda: print('Entered TCPEstablished state'),
            transitions=[
                Transition(event=Event.open, target=lambda: self.tcp_listen),
                ])

        self.tcp_listen = State(
            name='TCPListen',
            enter_action=lambda event: print('Entered TCPListen state'),
            transitions=[
                Transition(event=Event.acknowledge,
                           action=self.send_ack,
                           target=lambda: self.tcp_listen),
                Transition(event=Event.close, target=lambda: self.tcp_closed),
                ])

        self.tcp_closed = State(
            name='TCPClosed',
            enter_action=lambda event: print('Entered TCPClosed state'),
        )

        states = [
            self.tcp_established,
            self.tcp_listen,
            self.tcp_closed
        ]
        super().__init__(states)

    def send_ack(self, event):
        print('Executing TCPConnection.send_ack({})'.format(event))


def main():
    events = [Event.close, Event.acknowledge, Event.open,
              Event.acknowledge, Event.open, Event.acknowledge,
              Event.close, Event.acknowledge, Event.open]

    conn = TCPConnection()
    conn.start()

    # Some events will be ignored because they occur when the state machine
    # is in a state that has no transition for that event
    for event in events:
        conn.handle_event(event)


if __name__ == '__main__':
    main()
