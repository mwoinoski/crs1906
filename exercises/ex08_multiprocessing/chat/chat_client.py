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
        self.chat_room.add_message(self.name, message)

    def update(self, chat_msg):
        """Update this ChatClient with a new message from the ChatRoom."""
        print(f'\tMessage from {chat_msg.id}: {chat_msg.value}')
        print(prompt, end='', flush=True)

prompt = 'chat> '


def main():
    chat_room = None
    try:
        # from chat_room import ChatRoom
        from chat_room_proxy import ChatRoomProxy
        chat_room = ChatRoomProxy()
        client_name = input("What's your name? ")
        chat_client = ChatClient(client_name, chat_room)
        line = input(prompt)
        while line != 'quit':
            chat_client.new_message(line)
            line = input(prompt)

    except KeyboardInterrupt:  # user entered Ctrl-c
        pass
    except Exception as e:
        print('Exception:', e)
    finally:
        if chat_room:
            chat_room.shutdown()

if __name__ == '__main__':
    main()
