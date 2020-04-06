import logging
import logging.handlers

# Globals
logger = logging.getLogger('coimporter')
LOG_FILENAME = "coimporter.log"
MAX_SIZE_ROTATION = 1 * 1024 * 1024 # 1MB

def init_logging():
    """ Initialize the logging mechanism """
    logging.basicConfig(filename=LOG_FILENAME,
                        level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # Add the log message handler to the logger
    rotation_handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=MAX_SIZE_ROTATION, backupCount=5)

    logger.addHandler(rotation_handler)
    return logger


def log(msg):
    """ Writes msg in the logger output."""
    logging.info(msg)