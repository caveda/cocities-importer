import os
import logging

from cobroker import core

# Globals
logger = logging.getLogger('coimporter')


def set_environment():
    """ Set environment variables """
    with open('setupenv.sh') as f:
        processed = f.read().replace('export ', '')
    for line in processed.splitlines():
        var, _, value = line.partition('=')
        os.environ[var] = value.replace('"', '')


def init_logging():
    """ Initialize the logging mechanism """
    logger.setLevel(logging.INFO)
    return logger


def fetch_transport_data():
    """ By means of cobroker library, gathers the transport information. """
    logger.info("Fetching lines list...")
    lines = core.get_all_lines()
    logger.info(f"{len(lines)} lines.")
    for l in lines:
        logger.info(f"Collecting stops of line {l.id}")
        l.set_stops(core.get_line_stops(l))
        logger.info(f"Reading route of line {l.id}")
        l.set_route(core.get_line_route(l))
    logger.info(f"All information collected.")
    return lines


def main():
    """ Main function """
    init_logging()
    set_environment()
    lines = fetch_transport_data()
    for l in lines:
        print(l.to_json())


if __name__ == "__main__":
    main()
