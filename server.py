import asyncio
import logging
from parser import Parser
import os


class Server:
    def __init__(self, config, static_dir, workers):
        self.config = config
        self.static_dir = static_dir
        self.workers = workers
        self.loop = asyncio.get_event_loop()
        server_gen = asyncio.start_server(self.handle_connection, host=config["host"], port=config["port"],
                                          loop=self.loop)
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

    # def stop(self):
    #     if self.is_parent:
    #         print('server stopped')
    #         return
    #     os._exit(os.EX_OK)
