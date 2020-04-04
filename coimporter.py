import json
import os
from pathlib import Path

import logger
import time
import argparse
from datetime import timedelta
from zipfile import ZipFile, ZIP_DEFLATED
from codata_linter import sanitize
from logger import log
from cobroker import core, cologger
from utils import calculate_hash


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
    for i in range(2):
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


def generate_zip_file(file_to_zip, output_file):
    # Create a ZipFile Object
    with ZipFile(output_file, 'w',compression=ZIP_DEFLATED) as zipObj:
        zipObj.write(file_to_zip)
    log(f"Zip file {output_file} generated")
        


def parse_arguments():
    parser = argparse.ArgumentParser(description='Import transit data from CoCities.')
    parser.add_argument('output', nargs='?', help='Output file without extension. Both json and zip file will be generated.', default="alllines")
    return parser.parse_args()


def initialize_logging():
    logger.init_logging()
    cologger.set_logger(logger.logger)


def generate_metadata_file(data_file, meta_file):
    content = {'hash': calculate_hash(data_file), "time": str(time.time())}
    with open(meta_file, 'w') as f:
        json.dump(content, f)
    log(f"Metadata file {meta_file} generated")


def generate_output_files(lines, output):
    data_file = output + ".json"
    zip_file = output + ".zip"
    meta_file = output + "-meta.json"
    write_output_file(lines, data_file)
    generate_metadata_file(data_file,meta_file)
    generate_zip_file(data_file,zip_file)


def main():
    """ Main function """
    start = time.time()
    args = parse_arguments()
    initialize_logging()
    set_environment()
    lines = fetch_transport_data()
    generate_output_files(lines, args.output)
    elapsed = time.time() - start
    log(f"Execution time: {str(timedelta(seconds=elapsed))}")


if __name__ == "__main__":
    main()
