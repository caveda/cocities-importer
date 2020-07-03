import json
from cobroker.model import coordinates_to_locations


def parse_route(response):
    """ Parse json response containing the route of the line """
    data = json.loads(response)
    coordinates = []
    for part in data["features"][0]["geometry"]["coordinates"]:
        coordinates.extend(part)
    result = coordinates_to_locations(coordinates)
    return result

