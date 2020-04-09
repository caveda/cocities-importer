import concurrent.futures
import re

import requests
from cobroker import cocities, cologger
from cobroker.parser_connections import parse_connections
from cobroker.parser_lines import parse_lines
from cobroker.parser_routes import parse_route
from cobroker.parser_schedule import parse_schedule
from cobroker.parser_stops import parse_stops


def get_all_lines():
    """ Returns the complete list of lines without stops or routes. """
    query = cocities.get_request_all_lines()
    req = send_http_request(query)
    req.encoding = 'utf-8'  # force utf-8 encoding to preserve special chars
    lines = parse_lines(req.text)
    return lines


def get_line_stops(line):
    """ Returns the stops of the given line."""
    query = cocities.get_request_line_stops(line.id)
    req = send_http_request(query)
    stops = parse_stops(req.text, line)
    return stops


def get_stops_points(line):
    """ Returns an array with the locations of the line stops. """
    locations = map(lambda s: s.location, line.stops)
    return list(locations)


def get_line_route(l):
    """ Returns the complete list of lines without stops or routes. """
    try:
        query = cocities.get_request_line_route_map(l.get_line_request_unique_code())
        req = send_http_request(query)
        route = parse_route(req.text)
    except Exception as ex:
        # Route sometimes does not return anything. Return locations of stops as route.
        cologger.log(f"Exception captured fetching route of {l.get_client_line_id()}: {ex}")
        cologger.log(f"Replacing route by stops sequence.")
        route = get_stops_points(l)
    return route


def get_stop_schedule(l, s):
    """ Fills out the schedule of stop s of line line """
    max_retries = 3
    for i in range(max_retries - 1):
        try:
            query = cocities.get_request_stop_schedule(l.id, s.id, l.get_agency_direction_code())
            req = send_http_request(query)
            s.schedule = parse_schedule(req.text)
            break
        except Exception as ex:
            cologger.log(f"Exception captured fetching schedule of {l.get_client_line_id()}:{s.id}: {ex}")


def add_stops_static_schedule(line):
    """ Fills out the estimated schedule of each stop of the line """
    max_concurrency = 20
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrency) as executor:
        future_schedule = (executor.submit(get_stop_schedule, line, s) for s in line.stops)
        for f in concurrent.futures.as_completed(future_schedule):
            f.result()


def add_stops_connections(line):
    """ Adds to line the connections of each of its stops using the remote service """
    query = cocities.get_request_line_stops_info(line.get_line_request_unique_code())
    req = send_http_request(query)
    connections = parse_connections(req.text, line.id)
    for s in line.stops:
        s.set_connections(connections[s.id])


def add_stops_connections_from_cache(line, stops_connections):
    """ Adds to line the connections of each of its stops using the dict stops_connections """
    for s in line.stops:
        assert stops_connections.get(s.id) is not None, f"Stop {s.id} is not in connections cache"
        connections = list(filter(lambda x: re.match(f".{line.id}", x) is None, stops_connections[s.id]))
        s.set_connections(connections)


def send_http_request(query):
    """ Build a request out of the passed query. """
    return requests.request(query.method,
                            url=query.uri,
                            headers=query.headers,
                            data=query.body)
