import json
from cobroker.model import coordinates_to_locations


def parse_route(response):
    """ Parse json response containing the route of the line """
    data = json.loads(response)
    coordinates = get_line_feature_coordinates(data)
    result = coordinates_to_locations(coordinates)
    return result


def get_line_feature_coordinates (data):
    """ Searches the feature of the file that holds the full route and returns its index """
    result = []
    for i in range(data["totalFeatures"]):
        coordinates = parse_feature_coordinates(i, data)
        if len(coordinates) > len(result):
            result = coordinates
    return result


def parse_feature_coordinates(index, data):
    """ Extracts coordinates from the feature with the given index """
    coordinates = []
    for part in data["features"][index]["geometry"]["coordinates"]:
        coordinates.extend(part)
    return coordinates


