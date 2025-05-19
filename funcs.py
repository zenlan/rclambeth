
import os
import logging


def init_logger():
    filename, file_ext = os.path.splitext(os.path.basename(__file__))
    path = filename + ".log"
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(path, mode="w")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    return logger