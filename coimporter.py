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


def update_connections_with_line(stops_connections, l):
    """ Updates the dictionary stops_connections with the stops of the line l"""
    for s in l.stops:
        lines = stops_connections.get(s.id)
        if lines is None:
            stops_connections[s.id] = [l.get_client_line_id()]
        else:
            stops_connections[s.id].append(l.get_client_line_id())


def fetch_transport_data():
    """ By means of cobroker library, gathers the transport information. """
    log("Fetching lines list...")
    lines = core.get_all_lines()
    log(f"{len(lines)} lines.")
    stops_connections = dict()  # dictionary of stops and the lines they belong to (stopid:[lines])
    for i in range(len(lines)):
        l = lines[i]
        log(f"Fetching data of line {l.get_line_request_unique_code()}")
        log("  Collecting stops")
        l.set_stops(core.get_line_stops(l))
        log("  Reading route")
        update_connections_with_line(stops_connections, l)

    add_stops_connections(lines, stops_connections)

    log(f"All information collected.")
    return lines


def add_stops_connections(lines, stops_connections):
    """ Adds to lines stops the connections """
    for l in lines:
        log(f"Determining connections of line {l.get_line_request_unique_code()} stops")
        core.add_stops_connections_from_cache(l, stops_connections)


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
