"""
Demo of chat client that implements the Observer design pattern.
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

from ticketmanor.util.observer import Observer, Subject
from collections import namedtuple

ChatMessage = namedtuple('ChatMessage', 'id value')


class ChatHost(Subject):
    def __init__(self):
        super().__init__()
        self.messages = []

    def add_message(self, user_name, message):
        self.messages.append(ChatMessage(user_name, message))
        self.observer_notify()

    def how_many_messages(self):
        return len(self.messages)


class ChatClient(Observer):
    def __init__(self, name, chat_host):
        """Initialize the ChatClient"""
        super().__init__()
        self.name = name
        self.chat_host = chat_host
        self.last_msg_index = -1
        self.chat_host.observer_attach(self)

    def new_message(self, message):
        """Send a new message to the chat host"""
        print('{} sending message to ChatHost: {}'
              .format(self.name, message))
        self.chat_host.add_message(self.name, message)

    def update(self, _):
        """Update this ChatClient with new messages from the ChatHost"""
        how_many = self.chat_host.how_many_messages()
        new_messages = self.chat_host.messages[self.last_msg_index + 1:how_many]
        if new_messages:
            self.last_msg_index += len(new_messages)
            for message in [msg.value for msg in new_messages
                            if msg.id != self.name]:
                print('\t{} received message from ChatHost: {}'
                      .format(self.name, message))
