import fire
import json
import logging
import os
from server import Server


def main(config_path="/Users/MB-kochetkov/Projects/HTTP_server/config.json",
         static_dir="/Users/MB-kochetkov/Projects/HTTP_server", workers=4):
    logging.basicConfig(level=logging.INFO)
    logging.info("input: " + config_path + " " + static_dir + " " + str(workers))
    with open(config_path) as json_data:
        config = json.load(json_data)
    # for _ in range(workers - 1):
    #     if not os.fork():
    #         break
    Server(config, static_dir, workers)


if __name__ == '__main__':
    fire.Fire(main)
