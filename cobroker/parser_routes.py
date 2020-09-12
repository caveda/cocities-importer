import json
from cobroker.model import coordinates_to_locations


def parse_route(line, response):
    """ Parse json response containing the route of the line """
    data = json.loads(response)
    result = get_line_feature_coordinates(line, data)
    return result


def get_line_feature_coordinates(line, data):
    """ Searches the feature of the file that holds the full route and returns its index """
    result = []
    for i in range(data["totalFeatures"]):
        coordinates = parse_feature_coordinates(i, data)
        locations = coordinates_to_locations(coordinates)
        if line.check_route_include_all_stops(locations):
            result = locations
            break
    return result


def parse_feature_coordinates(index, data):
    """ Extracts coordinates from the feature with the given index """
    coordinates = []
    for part in data["features"][index]["geometry"]["coordinates"]:
        coordinates.extend(part)
    return coordinates


