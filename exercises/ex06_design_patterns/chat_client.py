"""
Demo of chat room client that implements the Observer design pattern.
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

from observer import Observer


class ChatClient(Observer):
    def __init__(self, name, chat_room):
        """Initialize the ChatClient"""
        # Observer constructor calls Subject.observer_attach()
        super().__init__(chat_room)
        self.name = name
        self.chat_room = chat_room

    def new_message(self, message):
        """Send a new message to the ChatRoom."""
        print('{} sending message: {}'
              .format(self.name, message))
        self.chat_room.add_message(self.name, message)

    def update(self, chat_msg):
        """Update this ChatClient with a new message from the ChatRoom."""
        print('\t{} received message: {}'
              .format(self.name, chat_msg))

if __name__ == '__main__':
    from chat_room import ChatRoom
    chat_room = ChatRoom()
    chat_client = ChatClient('Client 1', chat_room)
    prompt = 'chat> '
    line = input(prompt)
    while line != 'quit':
        chat_client.new_message(line)
        line = input(prompt)

# MW TODO: when modifying this client for remote proxy,
# add shutdown hook to close all sockets
