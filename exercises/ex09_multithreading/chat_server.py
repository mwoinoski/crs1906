"""
Simple (very simple!) socket-based chat server.
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

from threading import Lock
import sys
from socketserver import BaseRequestHandler, ThreadingTCPServer


class ChatServer(BaseRequestHandler):
    chat_sockets_lock = Lock()
    chat_sockets = set()

    def handle(self):
        print('Got connection from', self.client_address)
        with ChatServer.chat_sockets_lock:
            ChatServer.chat_sockets.add(self.request)
        while True:
            # wait for message from chat room proxy
            msg = self.request.recv(8192)
            if not msg:  # client closed socket
                self.request.shutdown()
                self.request.close()
                break
            # broadcast chat_msg to all other clients
            with ChatServer.chat_sockets_lock:
                for socket in ChatServer.chat_sockets:
                    if socket != self.request:
                        self.request.send(msg)

    @classmethod
    def shutdown(cls):
        with cls.chat_sockets_lock:
            for socket in cls.chat_sockets:
                socket.shutdown()
                socket.close()


def main():
    port = 20000
    # Allow server to rebind to previously used port number.
    ThreadingTCPServer.allow_reuse_address = True
    # Start server listening at localhost.
    # ThreadingTCPServer spawns a new thread to handle each connection request.
    server = ThreadingTCPServer(('', port), ChatServer)
    print('Starting ChatServer at port {}...'.format(port))
    server.serve_forever()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:  # catch Ctrl-c
        print('Shutting down chat server...')
        ChatServer.shutdown()
        sys.exit(0)

# for details of (lower-level) sockets, see
# https://docs.python.org/3.4/howto/sockets.html#non-blocking-sockets