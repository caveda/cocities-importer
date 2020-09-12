from xml.dom import minidom
from cobroker.model import Stop, Location, coordinates_to_locations, LINE_RETURN_DIRECTION
import re


def parse_stops(xml_response, line):
    """ Parse the response of all lines query """
    xml_stops = extract_stops_document(xml_response)
    xmldoc = minidom.parseString(xml_stops)
    stop_nodes = xmldoc.getElementsByTagName("DETALLE")
    result = []
    added_stops = set()
    coordinates = [] # Locations are stored to make a batch transformation which is way faster
    for s in stop_nodes:
        line_name = parse_stop_line_name(s)
        stop_id = parse_stop_id(s)
        if stop_id not in added_stops and stop_belongs_line(line, line_name):
            x, y = add_stop_without_duplicates(result, s, stop_id)
            added_stops.add(stop_id)
            coordinates.append((x,y))

    # Optimization: transform all stops coordinates at once
    if len(coordinates) > 0:
        transform_stops_coordinates(coordinates, result)
    return result


def transform_stops_coordinates(coordinates, stops):
    """ Updates stops with the locations transformed from coordinates """
    locations = coordinates_to_locations(coordinates)
    for i in range(len(locations)):
        stops[i].update_location(locations[i])


def add_stop_without_duplicates(result, s, stop_id):
    """ Adds stops without duplication """
    x, y = parse_stop_coordinates(s)
    stop = Stop(stop_id, parse_stop_name(s), Location(float(x), float(y)))
    result.append(stop)
    return x, y


def stop_belongs_line(line, stop_line_name):
    if len(line.get_destination_name()) > 1:
        destination = line.get_destination_name()
        pattern = f"^(fin de semana)(.+)\\({destination}\\)(.*)" if line.id == "76" \
            else f"^{destination}?|(semana|laborables|especial)(.+)\\({destination}\\)"
        return re.search(pattern, stop_line_name, re.IGNORECASE) is not None
    else:
        return True


def parse_stop_id(s):
    """ Parse a stop node to get the stop ID """
    id_node = s.getElementsByTagName("PARADAAUTOBUS")
    return id_node[0].firstChild.data


def parse_stop_name(s):
    """ Parse the stop node to get the name of the stop """
    name_node = s.getElementsByTagName("NOMBREPARADA")
    return name_node[0].firstChild.data


def parse_stop_line_name(s):
    """ Parse the line name of the stop. Used for filtering non-relevant nodes. """
    name_node = s.getElementsByTagName("NOMBRE")
    return name_node[0].firstChild.data


def extract_stops_document(xml_response):
    """ Extract the stops document from the response """
    xmldoc = minidom.parseString(xml_response)
    doc_stops = xmldoc.getElementsByTagName("valores")
    return doc_stops[0].firstChild.data


def parse_stop_coordinates(s):
    """ Parses the coordinates of the stop """
    xlo_node = s.getElementsByTagName("GEOMETRY_XLO")
    ylo_node = s.getElementsByTagName("GEOMETRY_YLO")
    return xlo_node[0].firstChild.data, ylo_node[0].firstChild.data
