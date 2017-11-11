import asyncio
import logging
from parser import Parser
import os
import socket


class Server:
    def __init__(self, config, static_dir, workers):
        self.config = config
        self.static_dir = static_dir
        self.workers = workers

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(False)
        self.socket.bind((self.config["host"], self.config["port"]))
        self.socket.listen(self.workers)
        for _ in range(self.workers - 1):
            if not os.fork():
                self.is_parent = False
                break

        self.loop = asyncio.get_event_loop()
        server_gen = asyncio.start_server(self.handle_connection, loop=self.loop, sock=self.socket)
        self.server = self.loop.run_until_complete(server_gen)
        logging.info('Listening established on {0}'.format(self.server.sockets[0].getsockname()))
        self.is_parent = True
        self.start()

    def start(self):

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass  # Press Ctrl+C to stop
        finally:
            # self.stop()
            self.server.close()
            self.loop.close()

    async def handle_connection(self, reader, writer):
        peername = writer.get_extra_info('peername')
        logging.info('Accepted connection from {}'.format(peername))
        request = await reader.read(self.config["buffer_size"])
        response = Parser(request, self.static_dir).parse()
        try:
            await writer.write(response)
        except Exception:
            pass
        writer.close()
