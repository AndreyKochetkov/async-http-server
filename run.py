import fire
import json
import logging
from server import Server


def main(config_path="/Users/mb-ott-1/HTTP_server/config.json",
         static_dir="/Users/mb-ott-1/HTTP_server", workers=4):
    logging.basicConfig(level=logging.INFO)
    logging.info("input: " + config_path + " " + static_dir + " " + str(workers))
    with open(config_path) as json_data:
        config = json.load(json_data)
    Server(config, static_dir, workers)


if __name__ == '__main__':
    fire.Fire(main)
