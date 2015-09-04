"""
GUI chat client that implements the Observer design pattern.
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

import tkinter as tk
from chat_client import Observer
from chat_room import ChatRoom

root = tk.Tk()

# TODO: ChatClientGui is a tkinter GUI chat client. Although the GUI code
# makes it more complex than the simple command client you completed before,
# you'll see that the Subject/Observer interaction is exactly the same as in
# the simpler chat client.
# (no code change required)

# TODO: make ChatClientGui a subclass of Observer
class ChatClientGui(Observer):
    last_y = 50

    # TODO: note the parameters to the ChatClientGui __init__() method
    # (no code changes required)
    def __init__(self, client_name, window, chat_room):
        self.create_widgets(client_name, window)

        # TODO: copy the 3 lines of code from the body of the
        # ChatClient __init__() method here
        super().__init__(chat_room)
        self.client_name = client_name
        self.chat_room = chat_room

    def callback(self, event):
        # TODO: note how we get the message text from the GUI's entry field.
        # (no code change required)
        message = self.entry_field.get()
        self.entry_field.delete(0, tk.END)
        print('got message ' + message)
        self.add_text('(me) ' + message + '\n')

        # TODO: call the ChatClientGui's new_message() method to send the text
        # from the entry field to the chat room
        self.new_message(message)

    def create_widgets(self, name, window):
        if window != root:
            window = tk.Toplevel(root)
        window.geometry('+200+{}'.format(ChatClientGui.last_y))
        ChatClientGui.last_y += 250
        window.wm_title(name)
        self.frame = tk.Frame(window)
        self.frame.grid()
        self.messaging_field = \
            tk.Text(self.frame, width=69, height=10, wrap=tk.WORD)
        self.messaging_field.grid(row=0, column=0, columnspan=2, sticky=tk.W)

        self.entry_field = tk.Entry(self.frame, width=92)
        self.entry_field.grid(row=1, column=0, sticky=tk.W)
        self.entry_field.bind('<Return>', self.callback)

        self.frame.pack()

    def add_text(self, data):
        self.messaging_field.insert(tk.END, data)

    # TODO: copy the new_message() method from ChatClient here
    def new_message(self, message):
        self.chat_room.add_message(self.client_name, message)

    # TODO: note that the update() method parameter list and the first 3 lines
    # of code are exactly the same as in the plain ChatClient class.
    # (no code change required)
    def update(self, chat_msg):
        id = chat_msg.id
        value = chat_msg.value
        print('\tMessage from {}: "{}"'.format(id, value))

        # TODO: note the call to add_text(), which adds the new chat message
        # to the client's output window
        # (no code change required)
        if self.client_name != chat_msg.id:
            self.add_text('({}) {}\n'.format(chat_msg.id, chat_msg.value))


def main():
    # TODO: create a ChatRoom instance and assign it to a variable named
    # `chat_host`
    chat_host = ChatRoom()

    # TODO: note the chat_host argument to the ChatClientGui constructor for
    # all three ChatClientGui instances
    # (no code change required)
    chat_client1 = ChatClientGui('Client 1', root, chat_host)
    chat_client2 = ChatClientGui('Client 2', chat_client1, chat_host)
    chat_client3 = ChatClientGui('Client 3', chat_client1, chat_host)

    root.mainloop()


if __name__ == '__main__':
    main()
