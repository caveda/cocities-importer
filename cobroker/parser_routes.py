import json

from cobroker.model import Location


def parse_route(response):
    """ Parse json response containing the route of the line """
    data = json.loads(response)
    coordinates = data["features"][0]["geometry"]["coordinates"][0]
    result = []
    for c in coordinates:
        result.append(Location.from_coordinates(c[0], c[1]))
    return result

