import logging

# Globals
logger = None


def set_logger(new_logger):
    """ Replaces the current logger by new logger """
    global logger
    logger = new_logger


def log(msg):
    """ Writes msg in the logger output."""
    if logger is not None:
        logger.info(msg)
