import json
import os
import logger
import time
import argparse
from datetime import timedelta

from codata_linter import sanitize
from logger import log
from cobroker import core


def set_environment():
    """ Set environment variables """
    with open('setupenv.sh') as f:
        processed = f.read().replace('export ', '')
    for line in processed.splitlines():
        var, _, value = line.partition('=')
        os.environ[var] = value.replace('"', '')


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
        log("  Adding static schedule")
        core.add_stops_static_schedule(l)

    add_stops_connections(lines, stops_connections)

    log(f"All information collected.")
    return lines


def add_stops_connections(lines, stops_connections):
    """ Adds to lines stops the connections """
    for l in lines:
        log(f"Determining connections of line {l.get_line_request_unique_code()} stops")
        core.add_stops_connections_from_cache(l, stops_connections)


def write_output_file(lines, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump([l.to_dict() for l in sanitize(lines)], f, ensure_ascii=False, indent=4)
    log(f"Output file {file_name} generated")


def parse_arguments():
    parser = argparse.ArgumentParser(description='Import transit data from CoCities.')
    parser.add_argument('output', nargs='?', help='Name of the output file', default="alllines.json")
    return parser.parse_args()


def main():
    """ Main function """
    start = time.time()
    args = parse_arguments()
    logger.init_logging()
    set_environment()
    lines = fetch_transport_data()
    write_output_file(lines, args.output)
    elapsed = time.time() - start
    log(f"Execution time: {str(timedelta(seconds=elapsed))}")


if __name__ == "__main__":
    main()
