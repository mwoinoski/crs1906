"""
chat_room.py - Defines a Subject subclass named ChatRoom for the Observer
design pattern example.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from observer import Subject
from collections import namedtuple


ChatMessage = namedtuple('ChatMessage', 'id value')


class ChatRoom(Subject):
    """
    ChatRoom extends Subject. It will be observed by ChatClient instances.
    """
    def __init__(self):
        super().__init__()
        self.messages = []

    # BONUS TODO: note that the ChatRoom.add_message() method is unchanged.
    #       The client calls this method exactly as before.
    #       (no code changes required)
    def add_message(self, user_name, message):
        chat_message = ChatMessage(user_name, message)
        self.messages.append(chat_message)
        self.observer_notify(chat_message)

    def shutdown(self):
        pass
