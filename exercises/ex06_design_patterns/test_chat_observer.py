"""
Unit tests for chat_client.py
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

from chat_client import ChatClient
from chat_room import ChatRoom, ChatMessage


def test_two_chat_clients():
    print()
    expected = [
        ChatMessage('client1', 'message 1'),
        ChatMessage('client2', 'message 2'),
        ChatMessage('client3', 'message 3'),
        ChatMessage('client3', 'message 4'),
        ChatMessage('client2', 'message 5'),
        ChatMessage('client1', 'message 6'),
    ]

    chat_host = ChatRoom()
    chat_client1 = ChatClient('client1', chat_host)
    chat_client2 = ChatClient('client2', chat_host)
    chat_client3 = ChatClient('client3', chat_host)

    chat_client1.new_message('message 1')
    chat_client2.new_message('message 2')
    chat_client3.new_message('message 3')
    chat_client3.new_message('message 4')
    chat_client2.new_message('message 5')
    chat_client1.new_message('message 6')

    actual = chat_host.messages

    assert expected == actual
