import asyncio
import logging
import concurrent.futures


class Server:
    def __init__(self, config, static_dir, workers):
        self.config = config
        self.static_dir = static_dir
        self.workers = workers
        self.loop = asyncio.get_event_loop()
        server_gen = asyncio.start_server(self.handle_connection, host=config["host"], port=config["port"], loop=self.loop)
        self.server = self.loop.run_until_complete(server_gen)
        logging.info('Listening established on {0}'.format(self.server.sockets[0].getsockname()))
        self.start()

    def start(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass  # Press Ctrl+C to stop
        finally:
            self.server.close()
            self.loop.close()

    async def handle_connection(self, reader, writer):
        peername = writer.get_extra_info('peername')
        logging.info('Accepted connection from {}'.format(peername))
        request = []
        while True:
            try:
                data = await asyncio.wait_for(reader.readline(), timeout=1.0)
                if data:
                    request.append(data.decode())
                else:
                    writer.write("some very important information".encode())
                    logging.info('Connection from {} closed by peer'.format(peername))
                    break
            except concurrent.futures.TimeoutError:
                logging.info('Connection from {} closed by timeout'.format(peername))
                break
        request = ''.join(request)
        request += "some data"
        writer.write(request.encode())
        writer.close()
