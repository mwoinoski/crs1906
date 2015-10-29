"""
test_tcp_connection.py - Unit tests for TcpConnection
"""

import unittest
from tcp_connection import TCPConnection, Event


class TestTcpConnection(unittest.TestCase):
    
    def test_tcp_connection(self):
        conn = TCPConnection()

        conn.start()  # initial state is established
        self.assertEqual(conn.tcp_established, conn.current_state)

        event_next_state_list = [
            (Event.close, conn.tcp_established),   # close before open: ignored
            (Event.acknowledge, conn.tcp_established), # acknowledge before open: ignored
            (Event.open, conn.tcp_listen),         # open connection
            (Event.acknowledge, conn.tcp_listen),  # send ack
            (Event.open, conn.tcp_listen),         # open in listen state: ignored
            (Event.acknowledge, conn.tcp_listen),  # send ack
            (Event.close, conn.tcp_closed),        # close connection
            (Event.acknowledge, conn.tcp_closed),  # acknowledge after close: ignored
            (Event.open, conn.tcp_closed),         # open after close: ignored
        ]

        for event, result_state in event_next_state_list:
            conn.handle_event(event)
            self.assertEqual(result_state, conn.current_state)


if __name__ == '__main__':
    unittest.main()
