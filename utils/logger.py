import os
import logging
from logging import handlers
import logging.config
from utils.path_manager import PathManager

MSG = """
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""


logs_path = PathManager.LOG_PATH + PathManager.PROJECT_NAME + ".log"
if os.path.exists(PathManager.LOG_PATH) is False:
    os.mkdir(PathManager.LOG_PATH)
if os.path.exists(logs_path) is False:
    file = open(logs_path, "w")
    file.write(MSG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

th = handlers.TimedRotatingFileHandler(
    filename=logs_path, when="MIDNIGHT", backupCount=30, encoding="utf-8"
)
ch = logging.StreamHandler()

ch.setLevel(logging.INFO)
formatter_fh = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s[line:%(lineno)d] - %(message)s"
)
ch.setFormatter(formatter_fh)
th.setFormatter(formatter_fh)
logger.addHandler(ch)
logger.addHandler(th)


if __name__ == "__main__":
    logger.info("hello logger")
