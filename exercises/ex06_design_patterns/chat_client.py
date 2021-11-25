"""
Demo of chat room client that implements the Observer design pattern.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from observer import Observer


# TODO: make ChatClient a subclass of Observer
class ChatClient:

    # TODO: note the parameters to the __init__() method
    # (no code change required)
    def __init__(self, client_name, chat_room):
        # The Observer constructor calls Subject.observer_attach()

        # TODO: call the superclass constructor, passing chat_room as the
        #       argument.
        ....

        # TODO: initialize a data attribute named `client_name` with the
        #       client_name parameter.
        ....

        # TODO: initialize a data attribute named `chat_room` with the
        #       chat_room parameter.
        ....

    def new_message(self, message):
        # TODO: call the chat_room's add_message() method, passing the
        #       client name from the client_name attribute and the message parameter.
        # HINT: the chat_room is stored in a data attribute
        ....

    # TODO: define the update() method, which overrides the abstract update()
    #       method in the Observer superclass.
    #       In addition to the "self" parameter, update() will have a second
    #       parameter that is a ChatMessage object.
    def ....
        # TODO: assign the ChatMessage's id attribute to a variable named `id`
        ....

        # TODO: assign the ChatMessage's value attribute to a variable named
        #       `value`
        ....

        # TODO: note the use of the ChatMessage's id and value in the following
        #       statement
        #       (no code change required)
        print(f'\tMessage from {id}: "{value}"')

        print(prompt, end='', flush=True)

prompt = 'chat> '


def main():
    chat_room = None
    try:
        # TODO: import ChatRoom from the chat_room module
        ....

        # TODO: create a ChatRoom() object and assign it to a variable
        #       named `chat_room`
        ....

        # BONUS TODO: comment out the two statements above (the import of
        #       ChatRoom and the setting of `chat_room`

        # BONUS TODO: import ChatRoomProxy from the chat_room_proxy module
        ....

        # BONUS TODO: create a ChatRoomProxy() object and assign it to a variable
        # named `chat_room`
        ....

        client_name = input("What's your name? ")

        # TODO: create a ChatClient object and assign it to a variable named
        #       `chat_client`. The ChatClient constructor takes two arguments:
        #       1. client_name
        #       2. chat_room
        ....

        # TODO: note how we read an input line from the console
        #       (no code change required)
        line = input(prompt)
        while line != 'quit':
            # TODO: call the ChatClient's new_message() method, passing the
            #       input line as the argument
            ....

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
