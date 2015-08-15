"""
chat_room_proxy.py - Defines a remote proxy for the ChatRoom.
The proxy has the same interface as the local ChatRoom, but the proxy sends
messages to a (potentially) remote server
"""

from observer import Subject
from collections import namedtuple

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

from chat_room import ChatRoom, ChatMessage
from socket import socket, AF_INET, SOCK_STREAM
import pickle
from threading import Thread


class ChatRoomProxy(ChatRoom):
    """
    ChatRoomProxy is a remote proxy for a chat room server.

    ChatRoomProxy implements the Subject interface, but will have only one
    Observer, a single ChatClient. ChatRoomProxy encapsulates the details
    of the network interactions, and presents an interface to the client
    exactly like a local instance of the ChatRoom class.
    """
    chat_server_port = 20000
    buf_size = 8096

    def __init__(self):
        """Initialize a connection with the remote ChatServer."""
        super().__init__()
        self.chat()

    # TODO: note the override of Subject.observer_notify().
    # This method is called by ChatRoom.add_message()
    def observer_notify(self, data):
        """
        Override of Subject.observer_notify() that pickles a ChatMessage and
        sends it to the ChatServer. The ChatServer will then broadcast
        notification of the new message to all clients (that is, all
        ChatRoomProxies).
        """
        serialized_msg = pickle.dumps(data)
        self.chat_socket.send(serialized_msg)

    def chat(self):
        """Spawn a thread to receive messages from the remote ChatServer."""
        self.chat_socket = socket(AF_INET, SOCK_STREAM)
        self.chat_socket.connect(('localhost', 20000))
        def receive_loop():
            while True:
                data = self.chat_socket.recv(ChatRoomProxy.buf_size)
                if data:
                    deserialized_msg = pickle.loads(data)
                    self.observer_notify(deserialized_msg)

        Thread(receive_loop).start()

