import time
import json
import logging


class ULog:
    def __init__(self):
        self.d = {}
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        self.logger = logger
        self.count = 0

    def _log(self, msg, level, time):
        self.d[self.count] = {"msg": msg, "level": level, "time": time}
        self.count += 1

    def debug(self, msg):
        self.logger.debug(msg)
        mc_time = time.time()
        self._log(msg, "debug", mc_time)

    def info(self, msg):
        self.logger.info(msg)
        mc_time = time.time()
        self._log(msg, "info", mc_time)

    def warning(self, msg):
        self.logger.warning(msg)
        mc_time = time.time()
        self._log(msg, "warning", mc_time)

    def error(self, msg):
        self.logger.warning(msg)
        mc_time = time.time()
        self._log(msg, "error", mc_time)

    def to_file(self, fpath):
        with open(fpath, "w") as outfile:
            json.dump(self.d, outfile)