import logging

# Globals
logger = logging.getLogger('coimporter')


def init_logging():
    """ Initialize the logging mechanism """
    logging.basicConfig(filename='coimporter.log',
                        level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    return logger


def log(msg):
    """ Writes msg in the logger output."""
    logging.info(msg)