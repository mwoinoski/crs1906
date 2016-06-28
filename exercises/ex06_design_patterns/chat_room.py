"""
chat_room.py - Defines a Subject subclass named ChatRoom for the Observer
design pattern example.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from observer import Subject
from collections import namedtuple

# TODO: Note the definition of the named tuple ChatMessage.
# A named tuple is basically a one-line class definition. It's an easy way to
# group several data values so they can be accessed by name instead of numeric
# index.
# (no code change required)
ChatMessage = namedtuple('ChatMessage', 'id, value')

""" TODO: You'll use ChatMessage in the methods below. Example:
>>> user_name = 'client 1'
>>> message = 'Greetings!'
>>> chat_message = ChatMessage(user_name, message)
>>> print('Message from {}: "{}"'.format(chat_message.id, chat_message.value))
Message from client 1: "Greetings!"
"""


# TODO: make ChatRoom a subclass of Subject
class ChatRoom:
    """
    ChatRoom extends Subject. It will be observed by ChatClient instances.
    """

    def __init__(self):
        # TODO: call the superclass constructor, passing no arguments
        # HINT: see slide 1-21
        ....

        # TODO: initialize a data attribute named `messages` with an empty list
        ....

    # TODO: note the definition of the add_message() method. Chat clients
    # call this method to send a message to the chat room.
    def add_message(self, user_name, message):

        # TODO: create a ChatMessage object and save it in a local variable.
        # Pass user_name and message as arguments to the ChatMessage
        # constructor.
        # HINT: see the definition of ChatMessage at the beginning of this file
        ....

        # TODO: append the ChatMessage to the list of messages in the
        # ChatRoom's "messages" attribute
        ....

        # TODO: call the ChatRoom's observer_notify() method, passing the
        # ChatMessage as the argument.
        ....


    # BONUS TODO: note that the ChatRoom.add_message() requires no changes.
    # The client calls this method exactly as before.
    # (no code changes required)

    def shutdown(self):
        pass
