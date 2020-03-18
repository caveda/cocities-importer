from xml.dom import minidom
from broker.model import LINE_FORWARD_DIRECTION, Line, Stop
import re

"""
  Parse the response of all lines query
"""


def parse_stops(xml_response, line):
    xml_stops = extract_stops_document(xml_response)
    xmldoc = minidom.parseString(xml_stops)
    stop_nodes = xmldoc.getElementsByTagName("DETALLE")
    result = []
    added_stops = set()
    for s in stop_nodes:
        line_name = parse_stop_line_name(s)
        stop_id = parse_stop_id(s)
        add_stop_without_duplicates(added_stops, line, line_name, result, s, stop_id)
    return result


def add_stop_without_duplicates(added_stops, line, line_name, result, s, stop_id):
    if stop_id not in added_stops and stop_belongs_line(line, line_name):
        stop = Stop(stop_id, parse_stop_name(s))
        result.append(stop)
        added_stops.add(stop_id)


def stop_belongs_line(line, stop_line_name):
    if len(line.get_destination_name()) > 1:
        pattern = f"^(Fin de Semana)(.+)\\({line.get_destination_name()}\\) y Retiradas" if line.id == "76" \
            else f"^{line.get_destination_name()}?|(semana|laborables|especial)(.+)\\({line.get_destination_name()}\\)"
        return re.search(pattern, stop_line_name, re.IGNORECASE) is not None
    else:
        return True


"""
    Parse a stop node to get the stop ID
"""
def parse_stop_id(s):
    id_node = s.getElementsByTagName("PARADAAUTOBUS")
    return id_node[0].firstChild.data


"""
    Parse the stop node to get the name of the stop
"""
def parse_stop_name(s):
    name_node = s.getElementsByTagName("NOMBREPARADA")
    return name_node[0].firstChild.data

"""
    Parse the line name of the stop. Used for filtering 
    non-relevant nodes.
"""
def parse_stop_line_name(s):
    name_node = s.getElementsByTagName("NOMBRE")
    return name_node[0].firstChild.data


"""
    Extract the stops document from the response
"""
def extract_stops_document(xml_response):
    xmldoc = minidom.parseString(xml_response)
    doc_stops = xmldoc.getElementsByTagName("valores")
    return doc_stops[0].firstChild.data
