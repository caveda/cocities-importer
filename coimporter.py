import json
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
    logging.basicConfig(filename='coimporter.log',
                        level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    return logger


def log(msg):
    logging.info(msg)


def fetch_transport_data():
    """ By means of cobroker library, gathers the transport information. """
    log("Fetching lines list...")
    lines = core.get_all_lines()
    log(f"{len(lines)} lines.")
    for i in range(3):
        l = lines[i]
        log(f"Collecting stops of line {l.get_line_request_unique_code()}")
        l.set_stops(core.get_line_stops(l))
        log(f"Reading route of line {l.get_line_request_unique_code()}")
        l.set_route(core.get_line_route(l))
    log(f"All information collected.")
    return lines


def write_output_file(lines):
    with open('alllines.json', 'w', encoding='utf-8') as f:
        json.dump([l.to_dict() for l in lines], f, ensure_ascii=False, indent=4)


def main():
    """ Main function """
    init_logging()
    set_environment()
    lines = fetch_transport_data()
    write_output_file(lines)


if __name__ == "__main__":
    main()
