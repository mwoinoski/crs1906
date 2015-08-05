"""
GUI chat client that implements the Observer design pattern.
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

import tkinter as tk
from ticketmanor.rest_services.chat_observer_demo import Observer, ChatHost

root = tk.Tk()


class ChatClientGui(Observer):
    last_x = 100

    # TODO: add a chat_host argument to the ChatClientGui constructor
    def __init__(self, name, window, chat_host):
        self.create_widgets(name, window)
        # TODO: copy the code from the body of the ChatClient constructor here
        super().__init__()
        self.name = name
        self.chat_host = chat_host
        self.last_msg_index = -1
        self.chat_host.observer_attach(self)

    def callback(self, event):
        message = self.entry_field.get()
        self.entry_field.delete(0, tk.END)
        print('got message ' + message)
        self.add_text(self.name + ': ' + message + '\n')
        # TODO: add a call to new_message() to add text from the entry field
        self.new_message(message)

    def create_widgets(self, name, window):
        if window != root:
            window = tk.Toplevel(root)
        window.geometry('+{}+200'.format(ChatClientGui.last_x))
        ChatClientGui.last_x += 600
        window.wm_title(name)
        self.frame = tk.Frame(window)
        self.frame.grid()
        self.messaging_field = \
            tk.Text(self.frame, width=69, height=20, wrap=tk.WORD)
        self.messaging_field.grid(row=0, column=0, columnspan=2, sticky=tk.W)

        self.entry_field = tk.Entry(self.frame, width=92)
        self.entry_field.grid(row=1, column=0, sticky=tk.W)
        self.entry_field.bind('<Return>', self.callback)

        self.frame.pack()

    def add_text(self, data):
        self.messaging_field.insert(tk.END, data)

    # TODO: copy the new_message() and update() methods from ChatClient here
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
            for chat_msg in [msg for msg in new_messages
                            if msg.id != self.name]:
                print('\t{} received message from ChatHost: {}'
                      .format(self.name, chat_msg))
                # TODO: add a call to add_text() here to add the message
                # to the output window
                self.add_text(chat_msg.id + ': ' + chat_msg.value + '\n')


def main():
    # TODO: create a ChatHost instance
    chat_host = ChatHost()

    # TODO: pass the ChatHost instance as an argument to the ChatClientGui
    # constructor
    chat_client1 = ChatClientGui('Client 1', root, chat_host)
    chat_client2 = ChatClientGui('Client 2', chat_client1, chat_host)

    root.mainloop()


if __name__ == '__main__':
    main()
