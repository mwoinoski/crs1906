"""
Unit tests for chat_server.py
"""
import time

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from unittest.mock import Mock, call
from chat_room import ChatMessage
from chat_room_proxy import ChatRoomProxy


def test_three_chat_clients():
    # Because we're testing the server, we can skip the chat client instances
    # and let the ChatRoomProxy take the role of client.
    chat_client1 = ChatRoomProxy()

    # If the server is working correctly, the ChatRoomProxy will call
    # the update() method of its single Observer. To confirm that, we'll
    # define a Mock observer and use its assert_has_calls() to verify that
    # the update() method was called correctly.
    observer1 = Mock()

    # Attach the Mock observer to the ChatRoomProxy.
    chat_client1.observer_attach(observer1)
    time.sleep(0.1)  # pause a bit, otherwise clients may miss messages

    chat_client2 = ChatRoomProxy()
    observer2 = Mock()
    chat_client2.observer_attach(observer2)
    time.sleep(0.1)

    chat_client3 = ChatRoomProxy()
    observer3 = Mock()
    chat_client3.observer_attach(observer3)
    time.sleep(0.1)

    # Send chat messages to the server from each "client"
    chat_client1.add_message('client1', 'message 1')
    chat_client2.add_message('client2', 'message 2')
    chat_client3.add_message('client3', 'message 3')
    chat_client3.add_message('client3', 'message 4')
    chat_client2.add_message('client2', 'message 5')
    chat_client1.add_message('client1', 'message 6')
    time.sleep(0.2)

    chat_client1.shutdown()
    chat_client2.shutdown()
    chat_client3.shutdown()

    # Verify that the Mock observer's update() method was called correctly.
    # A chat client should receive messages sent by other clients but should
    # not receive messages that it sent.
    observer1.update.assert_has_calls([
        call(ChatMessage('client2', 'message 2')),
        call(ChatMessage('client3', 'message 3')),
        call(ChatMessage('client3', 'message 4')),
        call(ChatMessage('client2', 'message 5')),
    ])

    observer2.update.assert_has_calls([
        call(ChatMessage('client1', 'message 1')),
        call(ChatMessage('client3', 'message 3')),
        call(ChatMessage('client3', 'message 4')),
        call(ChatMessage('client1', 'message 6')),
    ])

    observer3.update.assert_has_calls([
        call(ChatMessage('client1', 'message 1')),
        call(ChatMessage('client2', 'message 2')),
        call(ChatMessage('client2', 'message 5')),
        call(ChatMessage('client1', 'message 6')),
    ])
