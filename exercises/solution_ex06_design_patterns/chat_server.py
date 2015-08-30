"""
Simple (very simple!) socket-based chat server.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from threading import Lock
import atexit
from socketserver import BaseRequestHandler, ThreadingTCPServer


# TODO: note the definition of the ChatServer class, which defines a simple
# TCP socket-based chat server. A ChatServer co-ordinates conversations with
# chat clients running in different Python VMs, which may be connecting from
# different hosts across a network.
# (no code changes required)
class ChatServer(BaseRequestHandler):
    """
    ChatServer instances are created by ThreadingTCPServer.

    Each ChatServer instance handles a single client conversation.
    """
    chat_sockets_lock = Lock()
    chat_sockets = set()

    def handle(self):
        print('Got connection from', self.client_address)
        with ChatServer.chat_sockets_lock:
            ChatServer.chat_sockets.add(self.request)
        try:
            while True:
                # wait for message from chat client or chat room proxy
                msg = self.request.recv(8192)
                if not msg:  # client closed socket
                    break
                # broadcast msg to all other clients
                with ChatServer.chat_sockets_lock:
                    for socket in ChatServer.chat_sockets:
                        if socket != self.request:  # don't send msg to sender
                            socket.send(msg)
        except ConnectionError:  # client terminated abruptly
            pass
        finally:
            # the client closed the connection, so we'll remove the client's
            # socket from the chat_sockets set
            with ChatServer.chat_sockets_lock:
                ChatServer.chat_sockets.remove(self.request)
            if self.request:
                self.request.close()

    @classmethod
    def shutdown(cls):
        with cls.chat_sockets_lock:
            for socket in cls.chat_sockets:
                if socket:
                    socket.close()


@atexit.register
def shutdown_chat_server():
    print('Closing chat client sockets, ', end='')
    ChatServer.shutdown()
    print('shutting down chat server...')
    server.shutdown()


if __name__ == '__main__':
    try:
        port = 20000
        # Allow server to rebind to previously used port number.
        ThreadingTCPServer.allow_reuse_address = True
        # Start server listening at localhost. ThreadingTCPServer spawns a new
        # thread to handle each connection request.
        server = ThreadingTCPServer(('', port), ChatServer)
        print('Starting ChatServer at port {}...'.format(port))
        server.serve_forever()
    except KeyboardInterrupt:  # catch Ctrl-c
        pass  # Interpreter will call atexit handler

# for details of (lower-level) sockets, see
# https://docs.python.org/3.4/howto/sockets.html#non-blocking-sockets
