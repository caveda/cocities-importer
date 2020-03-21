import requests
from cobroker import cocities
from cobroker.parser_lines import parse_lines
from cobroker.parser_routes import parse_route
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


def get_line_route(line):
    """ Returns the complete list of lines without stops or routes. """
    query = cocities.get_request_line_route_map(line.get_line_request_unique_code())
    req = send_http_request(query)
    route = parse_route(req.text)
    return route


def send_http_request(query):
    """ Build a request out of the passed query. """
    return requests.request(query.method,
                            url=query.uri,
                            headers=query.headers,
                            data=query.body)
