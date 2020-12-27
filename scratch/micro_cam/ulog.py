import time
import json
import logging


class ULog:
    def __init__(self):
        self.d = {}
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        self.logger = logger

    def debug(self, msg):
        self.logger.debug(msg)
        self.d[time.time()] = msg

    def to_file(self, fpath):
        with open(fpath, "w") as outfile:
            json.dump(self.d, outfile)