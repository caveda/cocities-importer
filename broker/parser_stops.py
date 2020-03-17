
from xml.dom import minidom
from broker.model import LINE_FORWARD_DIRECTION, Line, Stop

"""
  Parse the response of all lines query
"""

def parse_stops (xml_response, line):
    xml_stops = extract_stops_document(xml_response)
    xmldoc = minidom.parseString(xml_stops)
    stop_nodes = xmldoc.getElementsByTagName("DETALLE")
    result =[]
    for s in stop_nodes:
        line_name = parse_stop_line_name(s)
        if line.get_destination_name().lower() in line_name.lower():
            stop = Stop(parse_stop_id(s), parse_stop_name(s))
            result.append(stop)
    return result

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