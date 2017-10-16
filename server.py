from parser import Parser
import os
import socket
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

from coroutine import Future, Task


def chunk_maker(sequence, chunk_size):
    while sequence:
        yield sequence[:chunk_size]
        sequence = sequence[chunk_size:]


class Server:
    def __init__(self, config, static_dir, workers):
        self.host = config.get('host')
        self.is_parent = True
        self.workers = workers
        self.num_of_users = config.get('num_of_users')
        self.port = config.get('port')
        self.receive_size = config.get('receive_chunk')
        self.static_dir = static_dir
        self.selector = None
        self.send_size = config.get('send_chunk')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def acceptor(self):
        try:
            conn, address = self.sock.accept()
            Task(self.handler(), conn)
        except Exception:
            return

    def start(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(False)
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.num_of_users)
        for _ in range(self.workers - 1):
            if not os.fork():
                self.is_parent = False
                break
        self.selector = DefaultSelector()
        self.selector.register(self.sock.fileno(), EVENT_READ, self.acceptor)

    def handler(self):
        future = Future()
        response = None
        connection = yield

        def readable():
            future.set_result(future)

        self.selector.register(connection, EVENT_READ, readable)
        yield future

        try:
            self.selector.unregister(connection)
            data = connection.recv(self.receive_size)
            response = Parser(data, self.static_dir).parse()
        except Exception:
            connection.close()

        def writable():
            future.set_result(future)

        self.selector.register(connection, EVENT_WRITE, writable)
        yield future

        self.selector.unregister(connection)
        try:
            for chunk in chunk_maker(response, self.send_size):
                connection.send(chunk)
                self.selector.register(connection, EVENT_WRITE, writable)
                yield future
                self.selector.unregister(connection)
        finally:
            connection.close()

    def stop(self):
        if self.is_parent:
            return
        os._exit(os.EX_OK)
