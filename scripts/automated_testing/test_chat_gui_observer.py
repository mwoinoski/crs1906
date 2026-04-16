"""
Automated GUI interaction tests for the tkinter chat client.
"""

import sys
import time
import threading
import tkinter as tk
from pathlib import Path
from socketserver import ThreadingTCPServer

EX06_ROOT = Path(__file__).resolve().parents[2] / "exercises" / "solution_ex06_design_patterns"
if str(EX06_ROOT) not in sys.path:
    sys.path.insert(0, str(EX06_ROOT))

import chat_gui_client
import chat_server
from chat_room import ChatMessage, ChatRoom
from chat_room_proxy import ChatRoomProxy


def _text(widget):
    return widget.get('1.0', tk.END)


def _cleanup_root(root):
    for child in list(root.winfo_children()):
        try:
            child.destroy()
        except tk.TclError:
            pass


def _wait_for(root, predicate, timeout=2.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        root.update()
        if predicate():
            return
        time.sleep(0.01)
    root.update()
    assert predicate()


def test_three_chat_client_guis_exchange_messages():
    root = chat_gui_client.root
    root.withdraw()
    _cleanup_root(root)

    chat_gui_client.ChatClientGui.last_y = 50
    chat_host = ChatRoom()

    client1 = chat_gui_client.ChatClientGui('Client 1', root, chat_host)
    client2 = chat_gui_client.ChatClientGui('Client 2', client1, chat_host)
    client3 = chat_gui_client.ChatClientGui('Client 3', client1, chat_host)

    client1.entry_field.insert(0, 'hello from 1')
    client1.callback(None)

    client2.entry_field.insert(0, 'reply from 2')
    client2.callback(None)

    _wait_for(root, lambda: '(Client 2) reply from 2\n' in _text(client1.messaging_field))

    assert chat_host.messages == [
        ChatMessage('Client 1', 'hello from 1'),
        ChatMessage('Client 2', 'reply from 2'),
    ]

    client1_text = _text(client1.messaging_field)
    client2_text = _text(client2.messaging_field)
    client3_text = _text(client3.messaging_field)

    assert '(me) hello from 1\n' in client1_text
    assert '(Client 2) reply from 2\n' in client1_text

    assert '(Client 1) hello from 1\n' in client2_text
    assert '(me) reply from 2\n' in client2_text

    assert '(Client 1) hello from 1\n' in client3_text
    assert '(Client 2) reply from 2\n' in client3_text

    _cleanup_root(root)


def test_three_networked_chat_client_guis_exchange_messages():
    root = chat_gui_client.root
    root.withdraw()
    _cleanup_root(root)
    chat_gui_client.ChatClientGui.last_y = 50

    ThreadingTCPServer.allow_reuse_address = True
    chat_server.ChatServer.chat_sockets = set()
    server = ThreadingTCPServer(('', ChatRoomProxy.chat_server_port), chat_server.ChatServer)
    chat_server.server = server
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    proxy1 = proxy2 = proxy3 = None
    try:
        proxy1 = ChatRoomProxy()
        proxy2 = ChatRoomProxy()
        proxy3 = ChatRoomProxy()

        client1 = chat_gui_client.ChatClientGui('Client 1', root, proxy1)
        client2 = chat_gui_client.ChatClientGui('Client 2', client1, proxy2)
        client3 = chat_gui_client.ChatClientGui('Client 3', client1, proxy3)

        client1.entry_field.insert(0, 'hello over socket')
        client1.callback(None)

        client2.entry_field.insert(0, 'reply over socket')
        client2.callback(None)

        _wait_for(
            root,
            lambda: '(Client 1) hello over socket\n' in _text(client3.messaging_field)
            and '(Client 2) reply over socket\n' in _text(client3.messaging_field),
        )

        client1_text = _text(client1.messaging_field)
        client2_text = _text(client2.messaging_field)
        client3_text = _text(client3.messaging_field)

        assert '(me) hello over socket\n' in client1_text
        assert '(Client 2) reply over socket\n' in client1_text

        assert '(Client 1) hello over socket\n' in client2_text
        assert '(me) reply over socket\n' in client2_text

        assert '(Client 1) hello over socket\n' in client3_text
        assert '(Client 2) reply over socket\n' in client3_text
    finally:
        for proxy in (proxy1, proxy2, proxy3):
            if proxy is not None:
                proxy.shutdown()
        server.shutdown()
        server.server_close()
        server_thread.join(timeout=1)
        chat_server.ChatServer.chat_sockets = set()
        _cleanup_root(root)
