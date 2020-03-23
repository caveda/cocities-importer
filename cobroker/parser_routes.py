import json
import logging

from cobroker.model import Location, coordinates_to_locations


def parse_route(response):
    """ Parse json response containing the route of the line """
    data = json.loads(response)
    coordinates = data["features"][0]["geometry"]["coordinates"][0]
    result = coordinates_to_locations(coordinates)
    return result

