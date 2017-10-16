import fire
import json
import logging

from server import Server


def main(config_path="/Users/MB-kochetkov/Projects/HTTP_server/config.json",
         static_dir="/Users/MB-kochetkov/Projects/HTTP_server", workers=4):
    logging.basicConfig(level=logging.INFO)
    logging.info("input: " + config_path + " " + static_dir + " " + str(workers))
    with open(config_path) as json_data:
        config = json.load(json_data)
    server = Server(config, static_dir, workers)
    server.start()
    try:
        while True:
            events = server.selector.select()
            for key, mask in events:
                callback = key.data
                callback()
    except KeyboardInterrupt:
        server.stop()


if __name__ == '__main__':
    fire.Fire(main)
