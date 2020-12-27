import time
import json
import logging


class ULog:
    """Wrapper around logger

    The default logger won't allow me to add a handler and so this wrapper will
    store an internal dict of the logger calls then allows them to be stored on
    a json file.
    """

    def __init__(self, name=__file__):
        self.d = {}
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(name)
        self.logger = logger
        self.count = 0
        self.name = name

    def _log(self, msg, level, time):
        self.d[self.count] = {
            "msg": msg,
            "level": level,
            "time": time,
            "name": self.name,
        }
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