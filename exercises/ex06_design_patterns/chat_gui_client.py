"""
GUI chat client that implements the Observer design pattern.
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

import tkinter as tk
from chat_client import Observer
from chat_room import ChatRoom

root = tk.Tk()


class ChatClientGui(Observer):
    last_y = 50

    # TODO: add a chat_room argument to the ChatClientGui init method
    def __init__(self, name, window, chat_room):
        self.create_widgets(name, window)
        # TODO: copy the code from the body of the ChatClient init method here
        super().__init__(chat_room)
        self.name = name
        self.chat_room = chat_room

    def callback(self, event):
        message = self.entry_field.get()
        self.entry_field.delete(0, tk.END)
        print('got message ' + message)
        self.add_text('(me) ' + message + '\n')
        # TODO: add a call to new_message() to add text from the entry field
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

    # TODO: copy the new_message() and update() methods from ChatClient here
    def new_message(self, message):
        """Send a new message to the ChatRoom"""
        print('{} sending message to ChatRoom: {}'
              .format(self.name, message))
        self.chat_room.add_message(self.name, message)

    def update(self, chat_msg):
        """Update this ChatClient with a new message from the ChatRoom"""
        print('\t{} received message from ChatRoom: {}'
              .format(self.name, chat_msg))
        # TODO: add code to implement the following pseudo-code:
        # 1. if chat_msg id is not equal to name of current ChatGuiClient:
        # 2. call add_text() to add the message to the output window
        if self.name != chat_msg.id:
            self.add_text('({}) {}\n'.format(chat_msg.id, chat_msg.value))


def main():
    # TODO: create a ChatRoom instance
    chat_host = ChatRoom()

    # TODO: add the ChatRoom instance as an additional argument to the
    # ChatClientGui constructor for all three ChatClientGui instances
    chat_client1 = ChatClientGui('Client 1', root, chat_host)
    chat_client2 = ChatClientGui('Client 2', chat_client1, chat_host)
    chat_client3 = ChatClientGui('Client 3', chat_client1, chat_host)

    root.mainloop()


if __name__ == '__main__':
    main()
